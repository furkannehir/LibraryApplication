<template>
  <div style="height: 100vh;">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">Authors</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="/books">Books</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-button @click="logout" variant="danger">Logout</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>


    <div class="container">
        <b-form-input v-model="searchTerm" placeholder="Search" class="mb-2"></b-form-input>
        <b-button @click="openAddAuthorDialog" :variant="authorDialogButtonVariant" class="mb-2">Add Author</b-button>
        <AddAuthor v-model="isAddAuthorVisible" />

        <b-row>
            <b-col cols="4" v-for="author in authors" :key="author.id">
                <b-list-group>
                    <b-list-group-item class="mb-2">
                    <h5>{{ author.name }}</h5>
                    <p>Book Count: {{ author.books.length }}</p>
                    <b-button @click="editAuthor(author.id)" variant="success">Edit</b-button>
                    <b-button @click="deleteAuthor(author.id)" variant="danger">Delete</b-button>
                    </b-list-group-item>
                </b-list-group>
            </b-col>
        </b-row>

        <div class="pagination">
            <b-pagination
                v-model="currentPage"
                :total-rows="totalPages"
                :per-page="1"
                aria-controls="my-table"
                class="my-2 fixed-bottom"
                @change="fetchAuthors"
            ></b-pagination>
        </div>  
    </div>


        <div class="back-drop" @click="cancelEdit" v-if="isEditDialogOpen"></div>
        <div class="edit-dialog" v-if="isEditDialogOpen">
            <h2>Edit Author</h2>
            <b-form @submit.prevent="updateAuthor(editedAuthor.id, editedAuthor)">
                <b-form-group label="Name:" label-for="edit-author-name">
                    <b-form-input v-model="editedAuthor.name" id="edit-author-name" required></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Update</b-button>
                <b-button @click="cancelEdit" variant="danger">Cancel</b-button>

                <!-- Book list -->
                <h3>Book List</h3>
                <b-list-group class="mb-2 book-list">
                    <b-list-group-item v-for="book in editedAuthor.books" :key="book.id">
                    <h5 class="mb-1">{{ book.name }}</h5>
                    <p>Page Number: {{ book.page_number }}</p>
                    <b-button @click="openEditDialog(book, editedAuthor.id)" variant="info">Edit</b-button>
                    <b-button @click="deleteBook(book.id)" variant="danger">Delete</b-button>
                    </b-list-group-item>
                </b-list-group>
                <b-button @click="addNewBook()" variant="primary">Add Book</b-button>

            </b-form>
    </div>


    <EditBook 
        :editedBook="editedBook" 
        :authors="authors.filter((author) => author.id === editedBook.author_id).map((author) => ({ id: author.id, label: author.name }))"
        v-model="isEditBookDialogOpen" 
    />
    <AddBook 
        v-model="isAddBookDialogOpen"
        :authors="authors.filter((author) => author.id === selected_author_id).map((author) => ({ id: author.id, label: author.name }))"
        :selected_author_id="selected_author_id"
    />
  </div>
</template>
    
<script>
  import EditBook from './editBook.vue';
  import AddBook from './addBook.vue';
  import AddAuthor from './addAuthor.vue';
  export default {
    components: {
        EditBook,
        AddBook,
        AddAuthor,
    },
    async asyncData({ params, query }) {
      const token = localStorage.getItem('token');
  
      if (!token) {
        return { authors: [], newAuthor: { name: '' } };
      }
  
      try {
        const authorsResponse = await fetch('http://localhost:8000/api/v1/authors', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
  
        const authors = await authorsResponse.json();
  
        return { authors, newAuthor: { name: '' } };
      } catch (error) {
        console.error('Error fetching data:', error);
        return { authors: [], newAuthor: { name: '' } };
      }
    },
    data() {
        return {
            authors: [],
            newAuthor: { name: '' },
            editedAuthor: { id: '', name: '' },
            isEditDialogOpen: false,
            isEditBookDialogOpen: false,
            isMenuOpen: false,
            isAddBookDialogOpen: false,
            currentPage: 1,
            totalPages: 1,
            pageSize: 20,
            editedBook: { name: '', page_number: '', author_id: '' },
            selected_author_id: '',
            isAddAuthorVisible: false,
            authorDialogButtonVariant: 'outline-info',
        };
    },
    async created() {
        this.newSearchTerm = '';
        await this.getPageCount();
        await this.fetchAuthors(1);
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
            this.fetchAuthors(1, newSearchTerm);
            this.getPageCount(newSearchTerm);

        },
    },
    methods: {
        async fetchAuthors(page, filter='') {
            if (page < 1 || page > this.totalPages) {
                return;
            }

            const token = localStorage.getItem('token');
            if (!token) {
                return;
            }

            try {
                const response = await fetch(
                    `http://localhost:8000/api/v1/authors?page=${page - 1}&pageSize=${this.pageSize}&filter=${filter}`,
                    {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    }
                );

                if (response.ok) {
                    const authors = await response.json();
                    this.authors = authors;
                    this.currentPage = page;
                } 
            } catch (error) {
            console.error('Error fetching authors:', error);
            }
        },

        async getPageCount(filter='') {
            const token = localStorage.getItem('token');
            if (!token) {
            return;
            }

            try {
            const response = await fetch(`http://localhost:8000/api/v1/authors/count?filter=${filter}`, {
                method: 'GET',
                headers: {
                Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const count = await response.json();
                if (count % this.pageSize === 0) {
                    this.totalPages = count / this.pageSize;
                } else {
                    this.totalPages = Math.floor(count / this.pageSize) + 1;
                }
            } else {
                console.error('Failed to fetch authors:', response.status);
            }
            } catch (error) {
            console.error('Error fetching authors:', error);
            }
        },
        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
        },
        logout() {
            localStorage.removeItem('token');
            this.$router.push('/login');
        },
        openAddAuthorDialog() {
            this.isAddAuthorVisible = !this.isAddAuthorVisible;
            if (this.isAddAuthorVisible) {
                this.authorDialogButtonVariant = 'info';
            } else {
                this.authorDialogButtonVariant = 'outline-info';
            }
        },
        editAuthor(authorId) {
            this.selected_author_id = authorId;
            console.log(this.selected_author_id);
            const authorToEdit = this.authors.find((author) => author.id === authorId);
            if (authorToEdit) {
            this.editedAuthor = { ...authorToEdit };
            this.isEditDialogOpen = true;
            }
        },
        async updateAuthor(authorId, updatedAuthor) {
            const token = localStorage.getItem('token');
            if (!token) {
                return;
            }
    
            const response = await fetch(`http://localhost:8000/api/v1/authors/${authorId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(updatedAuthor),
            });
    
            if (response.ok) {
                this.fetchAuthors(this.currentPage);
            } else {
                console.error('Failed to update the author:', response.status);
            }
            this.isEditDialogOpen = false;
        },
        cancelEdit() {
            this.isEditDialogOpen = false;
        },
        deleteAuthor(id) {
            const token = localStorage.getItem('token');
            if (!token) {
                return;
            }
    
            fetch(`http://localhost:8000/api/v1/authors/${id}`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${token}`,
            },
            })
            .then((response) => {
                if (response.ok) {
                    this.fetchAuthors(this.currentPage);
                } else {
                    console.error('Failed to delete author:', response.status);
                }
            })
            .catch((error) => {
                console.error('Error deleting author:', error);
            });
        },
        openEditDialog(book, authorId) {
            console.log(book);
            this.editedBook = { ...book };
            this.editedBook.author_id = authorId;
            this.isEditBookDialogOpen = true;
        },
        addNewBook(id) {
            this.isAddBookDialogOpen = true;
        },
    },
};
</script>

<style scoped lang="scss">
@import "./style.css";
    .authors-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: left;
        gap: 2rem;
        margin-bottom: 1.5rem;
        margin-top: 1.5rem;
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
    .form-input {
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 5px;
        margin-bottom: 0.3rem; 
        margin-right: 20px;
    }
    .book {
        padding: 1.5rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
        margin: 0.1rem 0;
    }

    .book:hover {
        transform: scale(1.02);
    }

    .book-title {
        font-size: 1.5rem;
        color: #333;
    }

    .book-info {
        font-size: 1rem;
        margin-bottom: 0.5rem;
        color: #555;
    }
    .book-list {
        height: 300px; /* Adjust this value as needed */
        overflow-y: auto;
    }
</style>
