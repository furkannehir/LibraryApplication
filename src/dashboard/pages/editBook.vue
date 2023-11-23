<!-- Edit Book Dialog -->
<template>
    <b-modal v-model="isVisible" @hide="cancelEdit" title="Edit Book" :hide-footer="true">
      <b-form @submit.prevent="updateBook(editedBook.id, editedBook)">
        <b-form-group label="Name:" label-for="edit-name">
          <b-form-input v-model="editedBook.name" id="edit-name" required></b-form-input>
        </b-form-group>
        <b-form-group label="Page Number:" label-for="edit-page-number">
          <b-form-input v-model="editedBook.page_number" id="edit-page-number" type="number" required></b-form-input>
        </b-form-group>
        <b-form-group label="Author:" label-for="edit-author">
            <treeselect
                    id="author"
                    v-model="editedBook.author_id"
                    :options="authors"
                    placeholder="Select an author"
                    :clearable="false"
                    required
                />
        </b-form-group>
        <b-button type="submit" variant="success">Update</b-button>
        <b-button @click="cancelEdit" variant="danger">Cancel</b-button>
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
        editedBook: {
            type: Object,
            required: true,
        },
        authors: {
            type: Array,
            required: true,
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
    methods: {

    cancelEdit() {
        this.isVisible = false;
    },
    async updateBook(bookId, updatedBook) {
        const token = localStorage.getItem('token');
        if (!token) {
            redirect('/login');
        }

        const response = await fetch(`http://localhost:8000/api/v1/books/${bookId}`, {
            method: 'PUT',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(updatedBook),
        });

        if (response.ok) {
            const response = await fetch('http://localhost:8000/api/v1/books', {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`,
            },
            });
            this.isVisible = false;
            const updatedBooksData = await response.json();
            this.books = updatedBooksData;
        } else {
            alert('Failed to update the book:', response.status);
        }
    },
  },

};
</script>

<style>
@import "./style.css";
</style>