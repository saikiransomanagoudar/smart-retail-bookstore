// store.js
import { configureStore } from "@reduxjs/toolkit";
import booksReducer from "./booksSlice"; // Adjust the path as needed

const store = configureStore({
  reducer: {
    books: booksReducer, // Add other reducers here if you have multiple slices
  },
});

export default store;
