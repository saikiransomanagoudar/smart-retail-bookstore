// booksSlice.js
import { createSlice } from "@reduxjs/toolkit";

const booksSlice = createSlice({
  name: "books",
  initialState: {
    trendingBooks: [],
    recommendedBooks: [],
  },
  reducers: {
    setTrendingBooks: (state, action) => {
      state.trendingBooks = action.payload;
    },
    setRecommendedBooks: (state, action) => {
      state.recommendedBooks = action.payload;
    },
  },
});

export const { setTrendingBooks, setRecommendedBooks } = booksSlice.actions;
export default booksSlice.reducer;
