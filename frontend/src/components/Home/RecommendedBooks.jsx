import { useEffect, useState } from "react";
import BookCard from "../Books/BookCard";
import axios from "axios";

const RecommendedBooks = () => {
  const [Books, setBooks] = useState();

  useEffect(() => {
    const fetch = async () => {
      const response = await axios.get(
        "http://localhost:1000/api/v1/initial-recommendations"
        // Replace with actual API for recommended books
      );
      setBooks(response.data.data);
    };
    fetch();
  }, []);

  return (
    <>
      {Books && (
        <div className='bg-zinc-900 px-12 py-8'>
          <h1 className='text-yellow-100 text-3xl'>Recommended Books</h1>
          <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 mt-8'>
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
