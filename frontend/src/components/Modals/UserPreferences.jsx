import { useState } from 'react';
import { useUser } from "@clerk/clerk-react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const UserPreferences = () => {
  const { user } = useUser();
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    favorite_books: [],
    favorite_authors: [],
    preferred_genres: [],
    themes_of_interest: [],
    reading_level: "intermediate"
  });

  // Predefined lists
  const popularBooks = [
    "The Great Gatsby", "1984", "Pride and Prejudice", 
    "To Kill a Mockingbird", "The Hobbit", "Harry Potter",
    "The Da Vinci Code", "The Alchemist", "The Catcher in the Rye",
    "Lord of the Rings", "The Hunger Games", "The Shining"
  ];

  const popularAuthors = [
    "J.K. Rowling", "Stephen King", "Jane Austen",
    "George R.R. Martin", "Agatha Christie", "Dan Brown",
    "Ernest Hemingway", "Mark Twain", "Charles Dickens",
    "Virginia Woolf", "George Orwell", "Paulo Coelho"
  ];

  const genres = [
    "Fiction", "Mystery", "Thriller", "Romance", "Science Fiction",
    "Fantasy", "Horror", "Historical Fiction", "Literary Fiction",
    "Young Adult", "Children's", "Biography"
  ];

  const themes = [
    "Adventure", "Love", "Family", "Friendship", "Coming of Age",
    "Good vs Evil", "Survival", "Redemption", "Identity", "Justice",
    "Power", "Nature"
  ];

  const readingLevels = [
    { value: "beginner", label: "Beginner" },
    { value: "intermediate", label: "Intermediate" },
    { value: "advanced", label: "Advanced" }
  ];

  const handleArraySelect = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(value)
        ? prev[field].filter(item => item !== value)
        : [...prev[field], value]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      await axios.post("http://localhost:8000/api/recommendations/preferences", {
        user_id: user.id,
        ...formData
      });
      navigate("/dashboard");
    } catch (error) {
      console.error("Error saving preferences:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Helper component for selectable buttons
  const SelectableButton = ({ value, selected, onClick, className }) => (
    <button
      type="button"
      onClick={onClick}
      className={`
        px-4 py-2 rounded-full text-sm font-medium transition-all duration-200
        ${selected 
          ? 'bg-indigo-100 text-indigo-700 border-2 border-indigo-500 shadow-inner' 
          : 'bg-white text-gray-700 border border-gray-300 hover:border-indigo-500 hover:bg-indigo-50'}
        ${className}
      `}
    >
      {value}
    </button>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white shadow-2xl rounded-2xl p-6 md:p-10">
          <div className="text-center mb-10">
            <h2 className="text-4xl font-bold text-gray-900 mb-2">Welcome to BookStore!</h2>
            <p className="text-xl text-gray-600">Help us personalize your reading experience</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Favorite Books */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-gray-900">
                Select Your Favorite Books
              </label>
              <div className="flex flex-wrap gap-2">
                {popularBooks.map(book => (
                  <SelectableButton
                    key={book}
                    value={book}
                    selected={formData.favorite_books.includes(book)}
                    onClick={() => handleArraySelect('favorite_books', book)}
                  />
                ))}
              </div>
            </div>

            {/* Favorite Authors */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-gray-900">
                Select Your Favorite Authors
              </label>
              <div className="flex flex-wrap gap-2">
                {popularAuthors.map(author => (
                  <SelectableButton
                    key={author}
                    value={author}
                    selected={formData.favorite_authors.includes(author)}
                    onClick={() => handleArraySelect('favorite_authors', author)}
                  />
                ))}
              </div>
            </div>

            {/* Preferred Genres */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-gray-900">
                Select Your Preferred Genres
              </label>
              <div className="flex flex-wrap gap-2">
                {genres.map(genre => (
                  <SelectableButton
                    key={genre}
                    value={genre}
                    selected={formData.preferred_genres.includes(genre)}
                    onClick={() => handleArraySelect('preferred_genres', genre)}
                  />
                ))}
              </div>
            </div>

            {/* Themes of Interest */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-gray-900">
                Select Themes That Interest You
              </label>
              <div className="flex flex-wrap gap-2">
                {themes.map(theme => (
                  <SelectableButton
                    key={theme}
                    value={theme}
                    selected={formData.themes_of_interest.includes(theme)}
                    onClick={() => handleArraySelect('themes_of_interest', theme)}
                  />
                ))}
              </div>
            </div>

            {/* Reading Level */}
            <div className="space-y-4">
              <label className="block text-lg font-semibold text-gray-900">
                Select Your Reading Level
              </label>
              <div className="flex gap-4">
                {readingLevels.map(level => (
                  <button
                    key={level.value}
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, reading_level: level.value }))}
                    className={`
                      flex-1 py-3 rounded-lg text-sm font-medium transition-all duration-200
                      ${formData.reading_level === level.value
                        ? 'bg-indigo-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}
                    `}
                  >
                    {level.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-6">
              <button
                type="submit"
                disabled={isSubmitting}
                className={`
                  w-full py-4 rounded-xl text-white font-medium text-lg
                  transition-all duration-200 transform hover:scale-[1.02]
                  ${isSubmitting
                    ? 'bg-indigo-400 cursor-not-allowed'
                    : 'bg-indigo-600 hover:bg-indigo-700 shadow-lg hover:shadow-xl'}
                `}
              >
                {isSubmitting ? 'Saving...' : 'Continue to Dashboard'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default UserPreferences;