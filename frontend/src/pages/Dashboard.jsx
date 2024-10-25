import { useEffect, useState } from "react";
import axios from "axios";
import BookCard from "../components/Books/BookCard";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { ClipLoader } from "react-spinners";
import UserPreferences from "../components/Modals/UserPreferences";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [popularBooks, setPopularBooks] = useState([]);
  const [recommendedBooks, setRecommendedBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userId] = useState(null);
  const navigate = useNavigate();

  const carouselSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 1,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1
        }
      }
    ]
  };

  useEffect(() => {
    const fetchUserPreferences = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/user-preferences/${userId}`);
        const preferences = response.data;
  
        if (preferences) {
          const recommendationsResponse = await axios.post(
            "http://localhost:8000/api/recommendations/initial-recommendations",
            preferences
          );
          const recommendationsData = recommendationsResponse.data || [];
          setRecommendedBooks(recommendationsData);
        } else {
          setIsModalOpen(true);
        }
      } catch (error) {
        console.error("Error fetching user preferences:", error);
      } finally {
        setLoading(false);
      }
    };
  
    fetchUserPreferences();
  }, [userId]);

  useEffect(() => {
    const fetchPopularBooks = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/recommendations/trending-books"
        );
        setPopularBooks(response.data);
      } catch (error) {
        console.error("Error fetching popular books:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPopularBooks();
  }, []);

  const handlePreferencesSubmitted = (recommendations) => {
    if (recommendations && Array.isArray(recommendations)) {
      setRecommendedBooks(recommendations);
    }

    setIsModalOpen(false);
  };

  useEffect(() => {
    const fetchUserPreferences = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/user-preferences/${userId}`);
        const preferences = response.data;
  
        if (preferences) {
          const recommendationsResponse = await axios.post(
            "http://localhost:8000/api/recommendations/initial-recommendations",
            preferences
          );
          const recommendationsData = recommendationsResponse.data || [];
          setRecommendedBooks(recommendationsData);
        } else {
          setIsModalOpen(true);
        }
      } catch (error) {
        console.error("Error fetching user preferences:", error);
      } finally {
        setLoading(false);
      }
    };
  
    fetchUserPreferences();
  }, [userId]);

  useEffect(() => {
    navigate("/dashboard");
  }, [navigate]);

  return (
    <div className="min-h-screen p-8 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-700 text-gray-100">
      <h1 className="text-4xl font-semibold mb-6 text-white">Dashboard</h1>

      {loading && (
        <div className="flex justify-center items-center h-64">
          <ClipLoader color="#ffffff" size={50} />
        </div>
      )}

      <UserPreferences
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onNext={handlePreferencesSubmitted}
      />

      {!loading && popularBooks.length > 0 && (
        <section className="mb-10">
          <h2 className="text-3xl font-semibold mb-4">Popular Books</h2>
          <Slider {...carouselSettings}>
            {popularBooks.map((book) => (
              <div key={book.id} className="px-2">
                <BookCard
                  bookid={book.id}
                  image={book.image_url}
                  title={book.title}
                  author={book.author || "Unknown Author"}
                  description={book.description || "No description available."}
                  price={book.price}
                />
              </div>
            ))}
          </Slider>
        </section>
      )}

      {!loading && recommendedBooks.length > 0 && (
        <section>
          <h2 className="text-3xl font-semibold mb-4">Recommended Books</h2>
          <Slider {...carouselSettings}>
            {recommendedBooks.map((book, index) => (
              <div key={index} className="px-2">
                <BookCard
                  bookid={book.id || index}
                  image={book.image_url || "default-image.jpg"}
                  title={book.title || "Unknown Title"}
                  author={book.author || "Unknown Author"}
                  description={book.description || "No description available."}
                  price={book.price || "Price not available"}
                />
              </div>
            ))}
          </Slider>
        </section>
      )}
    </div>
  );
};

export default Dashboard;
