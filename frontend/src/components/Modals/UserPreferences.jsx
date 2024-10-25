import { useState } from "react";
import PropTypes from "prop-types";
import axios from "axios";

const UserPreferences = ({ isOpen, onClose, onNext, userId }) => {
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedBook, setSelectedBook] = useState("");
  const [selectedAuthor, setSelectedAuthor] = useState("");
  const [themesOfInterest, setThemesOfInterest] = useState("");
  const [readingLevel, setReadingLevel] = useState("beginner");

  const bookOptions = [
    { title: "Harry Potter and the Sorcerer's Stone", author: "J.K. Rowling" },
    { title: "Harry Potter and the Chamber of Secrets", author: "J.K. Rowling" },
    { title: "The Hobbit", author: "J.R.R. Tolkien" },
    { title: "The Fellowship of the Ring", author: "J.R.R. Tolkien" },
    { title: "Dune", author: "Frank Herbert" },
    { title: "Foundation", author: "Isaac Asimov" },
    { title: "Neuromancer", author: "William Gibson" },
    { title: "Snow Crash", author: "Neal Stephenson" },
    { title: "The Da Vinci Code", author: "Dan Brown" },
    { title: "Angels & Demons", author: "Dan Brown" },
    { title: "Gone Girl", author: "Gillian Flynn" },
    { title: "The Girl with the Dragon Tattoo", author: "Stieg Larsson" },
    { title: "The Book Thief", author: "Markus Zusak" },
    { title: "All the Light We Cannot See", author: "Anthony Doerr" },
    { title: "Wolf Hall", author: "Hilary Mantel" },
    { title: "Bring Up the Bodies", author: "Hilary Mantel" },
    { title: "Pride and Prejudice", author: "Jane Austen" },
    { title: "Emma", author: "Jane Austen" },
    { title: "Outlander", author: "Diana Gabaldon" },
    { title: "Me Before You", author: "Jojo Moyes" }
  ];

  const genres = [
    "Art",
    "Biography",
    "Comics",
    "Children's",
    "Fantasy",
    "Horror",
    "Romance",
    "Science Fiction",
    "Thriller",
    "Travel"
  ];

  const handleGenreSelect = (genre) => {
    setSelectedGenres((prev) =>
      prev.includes(genre) ? prev.filter((g) => g !== genre) : [...prev, genre]
    );
  };

  const handleBookSelection = (event) => {
    const selected = bookOptions.find(
      option => `${option.title} by ${option.author}` === event.target.value
    );
    setSelectedBook(selected ? selected.title : "");
    setSelectedAuthor(selected ? selected.author : "");
  };

  const handleNext = async () => {
    const preferences = {
      user_id: userId,
      favorite_books: [selectedBook], 
      favorite_authors: [selectedAuthor],
      preferred_genres: selectedGenres,
      themes_of_interest: themesOfInterest.split(',').map(theme => theme.trim()), // Convert comma-separated string to list
      reading_level: readingLevel,
    };
  
    try {
      const llmResponse = await axios.post(
        "http://localhost:8000/api/recommendations/initial-recommendations",
        preferences
      );

      const recommendedBooks = llmResponse.data;
      onNext(recommendedBooks);

      await axios.post(
        "http://localhost:8000/api/recommendations/save-preferences",
        preferences
      );
  
    } catch (error) {
      console.error("Error sending user preferences:", error);
    }
  };
  
  return (
    isOpen && (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-md max-w-md w-full">
          <h2 className="text-2xl font-semibold mb-4 text-gray-800">
            Select Your Preferences
          </h2>

          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-800">
              Select Your Favorite Genres
            </h3>
            <div className="flex flex-wrap gap-2">
              {genres.map((genre) => (
                <button
                  key={genre}
                  onClick={() => handleGenreSelect(genre)}
                  className={`px-4 py-2 rounded-md ${
                    selectedGenres.includes(genre)
                      ? "bg-blue-500 text-white"
                      : "bg-gray-200 text-gray-800"
                  }`}
                >
                  {genre}
                </button>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 font-semibold mb-1">
              Choose a Favorite Book:
            </label>
            <select
              onChange={handleBookSelection}
              className="w-full p-2 border border-gray-300 rounded-md text-gray-800"
            >
              <option value="">Select a Book by Author</option>
              {bookOptions.map((option, index) => (
                <option key={index} value={`${option.title} by ${option.author}`}>
                  {option.title} by {option.author}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-gray-800 font-semibold mb-1">
              Themes of Interest (comma-separated):
            </label>
            <input
              type="text"
              value={themesOfInterest}
              onChange={(e) => setThemesOfInterest(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md text-gray-800"
              placeholder="e.g., Adventure, Mystery"
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-800 font-semibold mb-1">
              Reading Level:
            </label>
            <select
              value={readingLevel}
              onChange={(e) => setReadingLevel(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md text-gray-800"
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="flex justify-end mt-6">
            <button
              onClick={handleNext}
              className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
            >
              Next
            </button>
            <button
              onClick={onClose}
              className="ml-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    )
  );
};

UserPreferences.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onNext: PropTypes.func.isRequired,
  userId: PropTypes.number.isRequired
};

export default UserPreferences;
