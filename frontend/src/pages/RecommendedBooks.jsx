import React, { useEffect, useState } from "react";
import BookCard from "../components/Books/BookCard";
import axios from "axios";
import Loader from "./Loader";

const RecommendedBooks = () => {
  const [Books, setBooks] = useState();

  useEffect(() => {
    window.scrollTo(0, 0);
    const fetch = async () => {
      const response = await axios.get(
        "http://localhost:1000/api/v1/get-recommended-books"
        // Replace with actual API endpoint for recommended books
      );
      setBooks(response.data.data);
    };
    fetch();
  }, []);

  return (
    <>
      {!Books && <Loader />}
      {Books && (
        <div className='h-auto px-12 py-8 bg-zinc-900'>
          <h1 className='text-yellow-100 text-3xl mb-5'>Recommended Books</h1>
          <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8'>
            {Books.map((items, i) => (
              <BookCard
                bookid={items._id}
                image={items.url}
                title={items.title}
                author={items.author}
                price={items.price}
                key={i}
              />
            ))}
          </div>
        </div>
      )}
    </>
  );
};

export default RecommendedBooks;
