import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { FaCartShopping } from "react-icons/fa6";
import { GoHeartFill } from "react-icons/go";
import { GrLanguage } from "react-icons/gr";
import { MdDelete } from "react-icons/md";
import Loader from "./Loader";

const ViewBookDetails = () => {
  // const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [Book, setBook] = useState(location.state?.book || null);
  const { id } = useParams();

  useEffect(() => {
    // Update the book details whenever location.state.book changes
    if (location.state?.book) {
      setBook(location.state.book);
    } else if (!Book && !id) {
      // Redirect or handle the case when neither id nor book data is available
      navigate("/"); // Or any default route
    }
  }, [location.state?.book, id, navigate]);

  // Function to round rating to one decimal if it's present
  const roundedRating = Book?.rating ? Book.rating.toFixed(1) : null;

  const addToFavourite = async () => {
    console.log("Added to Favourite");
  };

  const addToCart = async () => {
    console.log("Added to Cart");
  };

  const deleteBook = async () => {
    console.log("Book Deleted");
    navigate("/all-books");
  };

  return (
    <>
      {!Book && <Loader />}
      {Book && (
        <div className='min-h-screen bg-gray-50 px-8 py-12 flex flex-col lg:flex-row items-center justify-center'>
          {/* Centering Wrapper */}
          <div className='flex flex-col lg:flex-row items-center justify-center w-full max-w-7xl gap-12'>
            {/* Image Section */}
            <div className='flex flex-col items-center lg:items-end w-full lg:w-1/2 max-w-lg mb-8 lg:mb-0'>
              <div className='bg-white rounded-lg shadow-lg p-4 relative overflow-hidden w-full h-full max-w-lg'>
                <img
                  src={Book.image_url}
                  alt={Book.title}
                  className='object-cover w-full h-[36rem] rounded-lg shadow-md'
                />
                <div className='absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent rounded-lg'></div>
                <div className='absolute top-2 right-2 bg-white text-gray-900 px-2 py-1 rounded-lg font-semibold shadow-lg'>
                  ${Book.price}
                </div>
                {Book.release_year && (
                  <div className='absolute bottom-2 left-2 text-xs font-semibold text-white bg-black/60 px-2 py-1 rounded-lg'>
                    {Book.release_year}
                  </div>
                )}
              </div>
            </div>

            {/* Divider Line */}
            <div className='hidden lg:block h-[36rem] w-0.5 bg-gray-300'></div>

            {/* Details Section */}
            <div className='w-full lg:w-1/2 max-w-xl text-left text-gray-900'>
              <h1 className='text-5xl font-bold mb-2 text-blue-900'>
                {Book.title}
              </h1>
              {Book.author && (
                <p className='text-2xl font-medium text-gray-700 mb-6'>
                  by {Book.author}
                </p>
              )}
              {Book.description && (
                <p className='text-lg text-gray-600 mb-6'>{Book.description}</p>
              )}
              {roundedRating && (
                <p className='text-2xl text-yellow-500 font-bold mb-4'>
                  ⭐ {roundedRating}/5
                </p>
              )}
              {Book.release_year && (
                <p className='text-lg text-gray-500 mb-4'>
                  Released Year: {Book.release_year}
                </p>
              )}
              {Book.release_date && (
                <p className='text-lg text-gray-500 mb-4'>
                  Released on:{" "}
                  {new Date(Book.release_date).toLocaleDateString()}
                </p>
              )}
              <div className='flex items-center text-gray-600 mb-4'>
                <GrLanguage className='mr-2' />
                <span>{Book.language || "English Language"}</span>
              </div>
              {Book.pages > 0 && (
                <p className='text-lg text-gray-600 mb-4'>
                  Pages: {Book.pages}
                </p>
              )}
              {Book.genres && (
                <p className='text-lg text-gray-600 mb-4'>
                  Genre:{" "}
                  {Array.isArray(Book.genres)
                    ? Book.genres.join(", ")
                    : Book.genres}
                </p>
              )}
              <p className='text-3xl text-blue-700 font-bold mb-8'>
                Price: ${Book.price}
              </p>

              {/* Action Buttons */}
              <div className='flex space-x-4'>
                <button
                  className='bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-all duration-300 flex items-center'
                  onClick={addToFavourite}
                >
                  <GoHeartFill className='mr-2' /> Add to Favourites
                </button>
                <button
                  className='bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 transition-all duration-300 flex items-center'
                  onClick={addToCart}
                >
                  <FaCartShopping className='mr-2' /> Add to Cart
                </button>
                <button
                  className='bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition-all duration-300 flex items-center'
                  onClick={deleteBook}
                >
                  <MdDelete className='mr-2' /> Delete Book
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ViewBookDetails;
