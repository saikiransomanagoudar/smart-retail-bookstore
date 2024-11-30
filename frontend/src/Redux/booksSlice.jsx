// booksSlice.js
import { createSlice } from "@reduxjs/toolkit";

const booksSlice = createSlice({
  name: "books",
  initialState: {
    trendingBooks: [],
    recommendedBooks: [],
    preferredGenres: [], 
  },
  reducers: {
    setTrendingBooks: (state, action) => {
      state.trendingBooks = action.payload;
    },
    setRecommendedBooks: (state, action) => {
      state.recommendedBooks = action.payload;
    },
    setPreferredGenres: (state, action) => {
      state.preferredGenres = action.payload; // Update preferredGenres
    },
  },
});

export const { setTrendingBooks, setRecommendedBooks, setPreferredGenres  } = booksSlice.actions;
export default booksSlice.reducer;
