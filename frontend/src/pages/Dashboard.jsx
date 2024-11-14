import React, { useEffect, useState } from "react";
import { useUser } from "@clerk/clerk-react";
import axios from "axios";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Chatbot from "../components/Chatbot/Chatbot";

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

const LoadingBookCard = ({ isCarousel = false }) => (
  <div className={isCarousel ? "mx-2" : ""}>
    <div className='bg-white rounded-xl shadow-md overflow-hidden'>
      <div className='relative h-52'>
        <div
          className='absolute inset-0 bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 animate-shimmer'
          style={{ backgroundSize: "200% 100%" }}
        />
        <div className='absolute top-2 right-2'>
          <div className='h-7 w-16 bg-white/90 rounded-lg' />
        </div>
        <div className='absolute top-2 left-2'>
          <div className='h-5 w-12 bg-black/20 rounded' />
        </div>
        <div className='absolute bottom-2 left-2 right-2'>
          <div className='h-4 bg-white/20 rounded w-3/4' />
        </div>
      </div>
      <div className='p-3'>
        <div className='flex items-center justify-between mb-2'>
          <div className='flex items-center gap-1'>
            <div className='h-4 w-4 bg-gray-200 rounded' />
            <div className='h-4 w-8 bg-gray-200 rounded' />
          </div>
          <div className='h-4 w-20 bg-gray-200 rounded' />
        </div>
        <div className='w-full h-8 bg-blue-50 rounded-lg' />
      </div>
    </div>
  </div>
);

const BookCard = ({
  image,
  title,
  rating,
  pages,
  price,
  releaseYear,
  isCarousel = false,
}) => {
  return (
    <div className={isCarousel ? "mx-2" : ""}>
      <div className='bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden transform hover:-translate-y-1'>
        <div className='relative h-52'>
          <img src={image} alt={title} className='w-full h-full object-cover' />
          <div className='absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent' />
          <div className='absolute top-2 right-2'>
            <div className='bg-white/90 backdrop-blur-sm text-gray-900 px-2.5 py-1 rounded-lg text-sm font-semibold shadow-lg'>
              ${price}
            </div>
          </div>
          <div className='absolute top-2 left-2'>
            <div className='bg-black/50 backdrop-blur-sm text-white px-2 py-0.5 rounded text-xs'>
              {releaseYear}
            </div>
          </div>
          <div className='absolute bottom-2 left-2 right-2'>
            <h3 className='text-white font-semibold text-sm line-clamp-2 drop-shadow-lg'>
              {title}
            </h3>
          </div>
        </div>
        <div className='p-3'>
          <div className='flex items-center justify-between mb-2'>
            <div className='flex items-center'>
              <span className='text-yellow-400 text-sm mr-1'>★</span>
              <span className='text-gray-700 text-sm font-medium'>
                {rating?.toFixed(1)}
              </span>
            </div>
            <div className='flex items-center text-gray-500 text-xs'>
              <span className='font-medium'>{pages} pages</span>
            </div>
          </div>
          <button
            className='w-full bg-blue-50 hover:bg-blue-100 text-blue-600 text-sm font-medium py-1.5 rounded-lg transition-colors duration-200'
            onClick={() => {
              /* Add your cart logic here */
            }}
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
  const [loadingRecommended, setLoadingRecommended] = useState(true);
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
        },
      },
      {
        breakpoint: 1280,
        settings: {
          slidesToShow: 4,
        },
      },
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 2,
        },
      },
      {
        breakpoint: 640,
        settings: {
          slidesToShow: 1,
        },
      },
    ],
  };

  // Fetch popular books
  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    const fetchPopularBooks = async () => {
      try {
        setLoadingPopular(true);
        const response = await axios.get(
          "http://localhost:8000/api/recommendations/trending-books",
          { signal: controller.signal }
        );
        if (isMounted) {
          setPopularBooks(response.data);
          localStorage.setItem("trendingBooks", JSON.stringify(response.data));
        }
      } catch (error) {
        if (error.name === "CanceledError") return;
        console.error("Error fetching popular books:", error);
      } finally {
        if (isMounted) {
          setLoadingPopular(false);
        }
      }
    };

    fetchPopularBooks();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, []); // No dependencies as this should only run once

  // Fetch recommended books when user changes
  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    const fetchRecommendedBooks = async () => {
      if (!user?.id) {
        setRecommendedBooks([]);
        setLoadingRecommended(false);

        return;
      }

      try {
        setLoadingRecommended(true);
        const response = await axios.post(
          "http://localhost:8000/api/recommendations/initial-recommendations",
          { userId: user.id },
          { signal: controller.signal }
        );

        if (isMounted) {
          setRecommendedBooks(response.data || []);
          localStorage.setItem(
            "recommendedBooks",
            JSON.stringify(response.data)
          );
        }
      } catch (error) {
        if (error.name === "CanceledError") return;
        console.error("Error fetching recommendations:", error);
      } finally {
        if (isMounted) {
          setLoadingRecommended(false);
        }
      }
    };

    fetchRecommendedBooks();

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, [user?.id]);

  return (
    <div className='min-h-screen bg-gray-50'>
      <style>{shimmerAnimation}</style>

      {/* Main Content */}
      <main className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'>
        {/* Popular Books Section */}
        <section className='mb-12' style={{ paddingTop: "3rem" }}>
          {" "}
          <div className='flex items-center justify-between mb-6'>
            <h2 className='text-xl font-semibold text-gray-900'>
              Popular Books
            </h2>
          </div>
          <div className='relative'>
            <Slider {...carouselSettings}>
              {loadingPopular
                ? Array(6)
                    .fill(null)
                    .map((_, index) => (
                      <LoadingBookCard key={index} isCarousel={true} />
                    ))
                : popularBooks.map((book) => (
                    <BookCard
                      key={book.id}
                      image={book.image_url}
                      title={book.title}
                      rating={book.rating}
                      pages={book.pages}
                      price={book.price}
                      releaseYear={book.release_year}
                      isCarousel={true}
                    />
                  ))}
            </Slider>
          </div>
        </section>
        {/* Recommended Books Section */}
        {user?.id && (
          <section className='mb-12'>
            <div className='flex items-center justify-between mb-6'>
              <h2 className='text-xl font-semibold text-gray-900'>
                Recommended for You
              </h2>
            </div>
            <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6'>
              {loadingRecommended
                ? Array(6)
                    .fill(null)
                    .map((_, index) => <LoadingBookCard key={index} />)
                : recommendedBooks.map((book) => (
                    <BookCard
                      key={book.id}
                      image={book.image_url}
                      title={book.title}
                      rating={book.rating}
                      pages={book.pages}
                      price={book.price}
                      releaseYear={book.release_year}
                    />
                  ))}
            </div>
          </section>
        )}
      </main>
      <Chatbot />
    </div>
  );
};

export default Dashboard;
