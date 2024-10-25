// Dashboard.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "@clerk/clerk-react";
import axios from "axios";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

// Shimmer Animation CSS
const shimmerAnimation = `
@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
.animate-shimmer {
  animation: shimmer 2s infinite linear;
}
`;

const LoadingBookCard = () => (
  <div className="mx-2">
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      {/* Image skeleton with gradient animation */}
      <div className="relative h-52">
        <div 
          className="absolute inset-0 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 animate-shimmer" 
          style={{ backgroundSize: '200% 100%' }} 
        />
        
        {/* Skeleton price tag */}
        <div className="absolute top-2 right-2">
          <div className="h-7 w-16 bg-white/90 rounded-lg" />
        </div>
        
        {/* Skeleton year tag */}
        <div className="absolute top-2 left-2">
          <div className="h-5 w-12 bg-black/20 rounded" />
        </div>
        
        {/* Skeleton title */}
        <div className="absolute bottom-2 left-2 right-2">
          <div className="h-4 bg-white/20 rounded w-3/4" />
        </div>
      </div>

      {/* Details section skeleton */}
      <div className="p-3">
        <div className="flex items-center justify-between mb-2">
          {/* Rating skeleton */}
          <div className="flex items-center gap-1">
            <div className="h-4 w-4 bg-gray-200 rounded" />
            <div className="h-4 w-8 bg-gray-200 rounded" />
          </div>
          
          {/* Pages skeleton */}
          <div className="h-4 w-20 bg-gray-200 rounded" />
        </div>

        {/* Button skeleton */}
        <div className="w-full h-8 bg-blue-50 rounded-lg" />
      </div>
    </div>
  </div>
);

const BookCard = ({ image, title, author, rating, pages, price, releaseYear }) => {
  return (
    <div className="mx-2">
      <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden transform hover:-translate-y-1">
        {/* Image Container */}
        <div className="relative h-52">
          <img
            src={image}
            alt={title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          
          {/* Price Tag */}
          <div className="absolute top-2 right-2">
            <div className="bg-white/90 backdrop-blur-sm text-gray-900 px-2.5 py-1 rounded-lg text-sm font-semibold shadow-lg">
              ${price}
            </div>
          </div>

          {/* Year Tag */}
          <div className="absolute top-2 left-2">
            <div className="bg-black/50 backdrop-blur-sm text-white px-2 py-0.5 rounded text-xs">
              {releaseYear}
            </div>
          </div>

          {/* Title on Image */}
          <div className="absolute bottom-2 left-2 right-2">
            <h3 className="text-white font-semibold text-sm line-clamp-2 drop-shadow-lg">
              {title}
            </h3>
          </div>
        </div>

        {/* Details Section */}
        <div className="p-3">
          <div className="flex items-center justify-between mb-2">
            {/* Rating */}
            <div className="flex items-center">
              <span className="text-yellow-400 text-sm mr-1">★</span>
              <span className="text-gray-700 text-sm font-medium">
                {rating?.toFixed(1)}
              </span>
            </div>
            
            {/* Pages */}
            <div className="flex items-center text-gray-500 text-xs">
              <span className="font-medium">{pages} pages</span>
            </div>
          </div>

          {/* Quick Action */}
          <button 
            className="w-full bg-blue-50 hover:bg-blue-100 text-blue-600 text-sm font-medium py-1.5 rounded-lg transition-colors duration-200"
            onClick={() => {/* Add your cart logic here */}}
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  );
};

const Dashboard = () => {
  const [popularBooks, setPopularBooks] = useState([]);
  const [recommendedBooks, setRecommendedBooks] = useState([]);
  const [loadingPopular, setLoadingPopular] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const { user } = useUser();

  const carouselSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 6,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    pauseOnHover: true,
    responsive: [
      {
        breakpoint: 1536,
        settings: {
          slidesToShow: 5,
        }
      },
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 4,
        }
      },
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
        }
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
        }
      },
      {
        breakpoint: 640,
        settings: {
          slidesToShow: 1,
        }
      }
    ]
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoadingPopular(true);
  
        // Fetch both popular books and recommendations concurrently
        const [popularResponse, recommendationsResponse] = await Promise.all([
          axios.get("http://localhost:8000/api/recommendations/trending-books"),
          user?.id 
            ? axios.post(
                "http://localhost:8000/api/recommendations/initial-recommendations",
                { userId: user.id }
              )
            : Promise.resolve({ data: [] })
        ]);
  
        setPopularBooks(popularResponse.data);
        setRecommendedBooks(recommendationsResponse.data || []);
  
      } catch (error) {
        console.error("Error fetching data:", error);
        if (error.response?.status === 404) {
          setIsModalOpen(true);
        }
      } finally {
        setLoadingPopular(false);
      }
    };
  
    fetchData();
  }, [user?.id]);

  const handlePreferencesSubmitted = (recommendations) => {
    if (recommendations && Array.isArray(recommendations)) {
      setRecommendedBooks(recommendations);
    }
    setIsModalOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <style>{shimmerAnimation}</style>
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-semibold text-gray-900">Book Store</h1>
            <nav className="flex space-x-6">
              <button className="text-gray-600 hover:text-gray-900 font-medium">Browse</button>
              <button className="text-gray-600 hover:text-gray-900 font-medium">Categories</button>
              <button className="text-gray-600 hover:text-gray-900 font-medium">Wishlist</button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Popular Books Section */}
        <section className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Popular Books</h2>
          </div>
          <div className="relative">
            <Slider {...carouselSettings}>
              {loadingPopular
                ? Array(6).fill(null).map((_, index) => (
                    <LoadingBookCard key={index} />
                  ))
                : popularBooks.map((book) => (
                    <BookCard
                      key={book.id}
                      bookid={book.id}
                      image={book.image_url}
                      title={book.title}
                      rating={book.rating}
                      pages={book.pages}
                      price={book.price}
                      releaseYear={book.release_year}
                    />
                  ))}
            </Slider>
          </div>
        </section>

        {/* Recommended Books Section */}
        {recommendedBooks.length > 0 && (
          <section className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Recommended for You</h2>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View All
              </button>
            </div>
            <div className="relative">
              <Slider {...carouselSettings}>
                {recommendedBooks.map((book) => (
                  <BookCard
                    key={book.id}
                    bookid={book.id}
                    image={book.image_url}
                    title={book.title}
                    rating={book.rating}
                    pages={book.pages}
                    price={book.price}
                    releaseYear={book.release_year}
                  />
                ))}
              </Slider>
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default Dashboard;