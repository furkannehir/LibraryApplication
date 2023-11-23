<template>
    <div v-if="isVisible">
        <b-form @submit.prevent="addNewAuthor">
            <b-form-group label="Author Name:" label-for="authorName">
            <b-form-input class="form-input" id="authorName" v-model="newAuthor.name" required></b-form-input>
            <b-button type="submit" variant="primary">Add</b-button>
            <b-button @click="cancelDialog" variant="danger">Cancel</b-button>        </b-form-group>
        </b-form>
    </div>
</template>

<script>
export default {
    props: {
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
        newAuthor: {
            name: '',
        },
      };
    },
    methods: {
        addNewAuthor() {
            const token = localStorage.getItem('token');
            this.$emit('addNewAuthor', this.newAuthor);
            this.newAuthor.name = '';
            fetch('http://localhost:8000/api/v1/author', {
            method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(this.newAuthor),
            })
            .then((response) => {
                if (response.ok) {
                return response.json();
                } else {
                return null;
                }
            })
            .then((newlyAddedAuthor) => {
                if (newlyAddedAuthor) {
                this.newAuthor.name = '';
                }
            })
            .then(() => {
                this.fetchAuthors(this.currentPage);
                this.getPageCount();
            })
            .catch((error) => {
                console.error('Error adding author:', error);
            });
        },
        cancelDialog() {
            this.isVisible = false;
        },
    },
};
</script>