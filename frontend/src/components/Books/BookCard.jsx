import PropTypes from "prop-types";

const BookCard = ({ image, title, author, price, description }) => {
  return (
    <div className="w-full transform hover:scale-105 transition-transform duration-300 cursor-pointer">
      <div className="bg-gray-800 text-white rounded-lg shadow-lg p-4 relative overflow-hidden hover:bg-gray-700 transition-colors duration-300 book-card">
        <div className="w-full flex items-center justify-center bg-gray-700 rounded-lg shadow-md mb-4 book-cover">
          <img
            src={image}
            alt="book"
            className="h-48 w-full object-cover rounded-lg book-image"
          />
        </div>
        <h1 className="mt-2 text-lg font-semibold">{title}</h1>
        <p className="mt-1 text-gray-300">by {author}</p>
        <p className="mt-1 text-gray-400">{description}</p>
        <p className="mt-1 text-gray-400">$ {price}</p>
      </div>
    </div>
  );
};

BookCard.propTypes = {
  image: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  author: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  price: PropTypes.number.isRequired,
};

export default BookCard;
