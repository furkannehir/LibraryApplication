<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Books</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="/authors">Authors</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-button @click="logout" variant="danger">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <div class="container">
      <b-form-input v-model="searchTerm" placeholder="Search" class="mb-2"></b-form-input>
      <b-button @click="openAddBookDialog" variant="info" class="mb-2">Add Book</b-button>
      <AddBook :authors="treeSelectAuthors" v-model="isAddBookVisible" />
      <b-row>
          <b-col cols="4" v-for="book in books" :key="book.id">
              <b-list-group>
                  <b-list-group-item class="mb-2">
                    <h5>{{ book.name }}</h5>
                    <p>Page Number: {{ book.page_number }}</p>
                    <p>Author: {{ book.author.name }}</p>
                    <b-button @click="openEditDialog(book.id)" variant="success">Edit</b-button>
                    <b-button @click="deleteBook(book.id)" variant="danger">Delete</b-button>
                  </b-list-group-item>
              </b-list-group>
          </b-col>
        </b-row>

      <b-pagination
        v-model="currentPage"
        :total-rows="totalPages"
        :per-page="1"
        aria-controls="my-table"
        class="my-2 fixed-bottom"
        @change="fetchBooks"
      ></b-pagination>
    </div>

    <EditBook 
      :edited-book="editedBook" 
      :authors="authors.map((author) => ({ id: author.id, label: author.name }))" 
      v-model="isEditDialogOpen" 
    />
  </div>
</template>
  
<script>
import EditBook from './editBook.vue';
import AddBook from './addBook.vue';


export default {
  components: {
    EditBook,
    AddBook,
  },
  async asyncData({ params, query }) {
    const token = localStorage.getItem('token');
    let pageSize = 6; 

    if (query.page_size) {
      pageSize = parseInt(query.page_size, 10);
    }

    if (!token) {
      return { books: [], authors: [], newBook: { author_id: '', name: '', page_number: 0 } };
    }

    try {
      const [booksResponse, authorsResponse] = await Promise.all([
        fetch(`http://localhost:8000/api/v1/books?page=0&pageSize=${pageSize}`, {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }),
        fetch('http://localhost:8000/api/v1/authors', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }),
      ]);

      const [books, authors] = await Promise.all([booksResponse.json(), authorsResponse.json()]);
      const treeSelectAuthors = authors.map((author) => {
        return { id: author.id, label: author.name };
      });
      return { books, authors, treeSelectAuthors, newBook: { author_id: '', name: '', page_number: 0 } };
    } catch (error) {
      console.error('Error fetching data:', error);
      return { books: [], authors: [], treeSelectAuthors: [], newBook: { author_id: '', name: '', page_number: 0 } };
    }
  },
  data() {
    return {
      currentPage: 1,
      books: [],
      selectedBook: null,
      authors: [],
      treeSelectAuthors: [],
      newBook: { author_id: '', name: '', page_number: 0 },
      editedBook: { id: '', author_id: '', name: '', page_number: 0 },
      isEditDialogOpen: false,
      isMenuOpen: false,
      isAddBookVisible: false,
      totalPages: 1,
      pageSize: 9,
    };
  },
  async created() {
    this.searchTerm = '';
    await this.getPageCount();
    await this.fetchBooks(1);
  },
  mounted() {
    this.searchTerm = '';
  },
  computed: {
    searchTerm: {
        get() {
            return this.$store.state.searchTerm;
        },
        set(newSearchTerm) {
            this.$store.commit('setSearchTerm', newSearchTerm);
        },
      },
    },
  watch: {
    searchTerm(newSearchTerm) {
      this.fetchBooks(1, newSearchTerm);
      this.getPageCount(newSearchTerm);
    },
  },
  methods: {
    
    openAddBookDialog() {
      this.isAddBookVisible = true;
    },

    async getPageCount(filter = '') {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/books/count?&filter=${filter}`,
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const count = await response.json();
          if (count % this.pageSize === 0) {
            this.totalPages = count / this.pageSize;
          } else {
            this.totalPages = Math.floor(count / this.pageSize) + 1;
          }
        }
      } catch (error) {
        console.error(error);
      }
    },
    async fetchBooks(page, filter = '') {
      if (this.currentPage < 1 || this.currentPage > this.totalPages) {
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }

      try {
        const response = await fetch(
          `http://localhost:8000/api/v1/books?page=${page - 1}&pageSize=${this.pageSize}&filter=${filter}`,
          {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (response.ok) {
          const books = await response.json();
          this.books = books;
        }
      } catch (error) {
        console.error(error);
      }
    },
    deleteBook(id) {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }

      fetch(`http://localhost:8000/api/v1/books/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            return null;
          }
        })
        .then((deletedBook) => {
          if (deletedBook) {
            this.books = this.books.filter((book) => book.id !== deletedBook.id);
          }
        })
        .catch((error) => {
          console.error('Error deleting book:', error);
        });
    },
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
    // Add methods for handling pagination
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.books && this.currentPage * this.pageSize < this.books.length) {
        this.currentPage++;
      }
    },

    openEditDialog(bookId) {
      const bookToEdit = this.books.find((book) => book.id === bookId);
      if (bookToEdit) {
        this.editedBook = { ...bookToEdit };
        this.editedBook.author_id = this.editedBook.author.id;
        this.isEditDialogOpen = true;
      }
      this.isEditDialogOpen = true;
      },
  },
};
</script>
  
  <style scoped lang="scss">
  /* Your existing styles */
  .books-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: flex-start;
    gap: 2rem;
    margin-bottom: 1.5rem;
  }

.hamburger-menu {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 25px;
  height: 20px;
  margin-right: 10px;

  .bar {
    background-color: #333;
    height: 3px;
    width: 100%;
  }
}

.hamburger-menu-container {
  width: 100%;
  display: flex;
  justify-content: right;
  align-items: center;
  margin-top: 20px;
}

/* Menu options style */
.menu-options {
  position: absolute;
  top: 40px;
  right: 10px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: none;
  z-index: 1000;

  &.open {
    display: block;
  }
}
</style>
  