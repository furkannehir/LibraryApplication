<template>
    <b-modal v-model="isVisible" @hide="cancelDialog" title="Add Book" :hide-footer="true">
      <b-form @submit.prevent="addBook">
        <b-form-group label="Select an Author:" label-for="author">
          <treeselect
            id="author"
            v-model="selected_author_id"
            :options="authors"
            placeholder="Select an author"
            :clearable="false"
            required
          />
        </b-form-group>
        <b-form-group label="Book Name:" label-for="name">
          <b-form-input id="name" v-model="newBook.name" required></b-form-input>
        </b-form-group>
        <b-form-group label="Page Number:" label-for="page-number">
          <b-form-input id="page-number" v-model="newBook.page_number" type="number" required></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="success">Add Book</b-button>
        <b-button @click="cancelDialog" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </template>

<script>
import Treeselect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css';

export default {
  components: {
    Treeselect,
  },
    props: {
        authors: {
            type: Array,
            required: true,
        },
        selected_author_id: {
            type: Number,
            required: false,
        },
        value: {
            type: Boolean,
            required: false,
            default: false,
        },
    },
    computed: {
        isVisible: {
            get() {
                return this.value;
            },
            set(newValue) {
                this.$emit('input', newValue);
            },
        },
    },
    data() {
      return {
        newBook: {
          name: '',
          page_number: 0,
          author_id: this.selected_author_id,
        },
      };
    },
    methods: {
        addBook() {
            const token = localStorage.getItem('token');

            if (!token) {
                return;
            }

            fetch('http://localhost:8000/api/v1/book', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(this.newBook),
            })
                .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    return null;
                }
                })
                .then((newlyAddedBook) => {
                if (newlyAddedBook) {
                    this.newBook.author_id = '';
                    this.newBook.name = '';
                    this.newBook.page_number = 0;
                }
                })
                .then(() => {
                this.fetchBooks(this.currentPage);
                this.getPageCount();
                })
                .catch((error) => {
                console.error('Error adding book:', error);
                });
            this.isVisible = false;
        },
        cancelDialog() {
            this.isVisible = false;
        },
    },
};
</script>

<style scoped>
@import "./style.css";
</style>