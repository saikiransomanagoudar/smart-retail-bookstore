import React, { useEffect, useState } from "react";
import { useUser } from "@clerk/clerk-react";
import axios from "axios";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import Chatbot from "../components/Chatbot/Chatbot";
import { setTrendingBooks, setRecommendedBooks } from "../Redux/booksSlice";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";

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
          <img 
            src={image || "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+"} 
            alt={title} 
            className='w-full h-full object-cover'
            onError={(e) => {
              e.target.src = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDMwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9ImJnR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNjY2Njk5O3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM5OTk5Y2M7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGxpbmVhckdyYWRpZW50IGlkPSJib29rR3JhZGllbnQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojNDA0NjhiO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM2MjY2OWY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICA8L2xpbmVhckdyYWRpZW50PgogICAgPGZpbHRlciBpZD0iZHJvcFNoYWRvdyI+CiAgICAgIDxmZU9mZnNldCBkeD0iMyIgZHk9IjMiLz4KICAgICAgPGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMyIvPgogICAgICA8ZmVGbG9vZCBmbG9vZC1jb2xvcj0iIzAwMDAwMCIgZmxvb2Qtb3BhY2l0eT0iMC4zIi8+CiAgICAgIDxmZUNvbXBvc2l0ZSBvcGVyYXRvcj0ib3ZlciIvPgogICAgPC9maWx0ZXI+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iNDAwIiBmaWxsPSJ1cmwoI2JnR3JhZGllbnQpIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDgwKSI+CiAgICA8IS0tIEJvb2sgQ292ZXIgLS0+CiAgICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTUwIiBoZWlnaHQ9IjI0MCIgZmlsbD0idXJsKCNib29rR3JhZGllbnQpIiByeD0iMTAiIGZpbHRlcj0idXJsKCNkcm9wU2hhZG93KSIvPgogICAgPCEtLSBCb29rIFNwaW5lIC0tPgogICAgPHJlY3QgeD0iNSIgeT0iMCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjI0MCIgZmlsbD0iIzJkMzc0OCIgcng9IjIiLz4KICAgIDwhLS0gQm9vayBQYWdlcyAtLT4KICAgIDxyZWN0IHg9IjE1IiB5PSI4IiB3aWR0aD0iMTI1IiBoZWlnaHQ9IjIyNCIgZmlsbD0iI2Y4ZjlmYSIgcng9IjUiLz4KICAgIDwhLS0gVGV4dCBMaW5lcyAtLT4KICAgIDxyZWN0IHg9IjI1IiB5PSIzMCIgd2lkdGg9IjEwNSIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjQ1IiB3aWR0aD0iODAiIGhlaWdodD0iNCIgZmlsbD0iI2UwZTZlZCIgcng9IjIiLz4KICAgIDxyZWN0IHg9IjI1IiB5PSI2MCIgd2lkdGg9Ijk1IiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNzUiIHdpZHRoPSI3MCIgaGVpZ2h0PSI0IiBmaWxsPSIjZTBlNmVkIiByeD0iMiIvPgogICAgPHJlY3QgeD0iMjUiIHk9IjkwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQiIGZpbGw9IiNlMGU2ZWQiIHJ4PSIyIi8+CiAgICA8IS0tIEJvb2sgSWNvbiAtLT4KICAgIDxjaXJjbGUgY3g9Ijc1IiBjeT0iMTYwIiByPSIyNSIgZmlsbD0iIzQwNDY4YiIgb3BhY2l0eT0iMC4xIi8+CiAgICA8dGV4dCB4PSI3NSIgeT0iMTcwIiBmb250LWZhbWlseT0iU2Vnb2UgVUksIEFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjMwIiBmaWxsPSIjNDA0NjhiIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OWPC90ZXh0PgogIDwvZz4KPC9zdmc+";
            }}
          />
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
  const dispatch = useDispatch();
  // const [popularBooks, setPopularBooks] = useState([]);
  // const [recommendedBooks, setRecommendedBooks] = useState([]);
  const [loadingPopular, setLoadingPopular] = useState(true);
  const [loadingRecommended, setLoadingRecommended] = useState(true);
  const { user } = useUser();
  const popularBooks = useSelector((state) => state.books.trendingBooks);
  const recommendedBooks = useSelector((state) => state.books.recommendedBooks);
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
          // setPopularBooks(response.data);
          dispatch(setTrendingBooks(response.data));
          // console.log(`trendingBooks`, response.data);
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
          dispatch(setRecommendedBooks(response.data || []));

          // console.log(`initial-recommendations`, response.data);
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
    <div className="min-h-screen bg-gray-50">
      <style>{shimmerAnimation}</style>
  
      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Popular Books Section */}
        <section className="mb-12" style={{ paddingTop: "3rem" }}>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Popular Books</h2>
          </div>
          <div className="relative">
            <Slider {...carouselSettings}>
              {loadingPopular
                ? Array(6)
                    .fill(null)
                    .map((_, index) => (
                      <LoadingBookCard key={`loading-popular-${index}`} isCarousel={true} />
                    ))
                : popularBooks.map((book, index) => (
                    <BookCard
                      key={book.id || `popular-${index}`}
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
          <section className="mb-12">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Recommended for You</h2>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
              {loadingRecommended
                ? Array(6)
                    .fill(null)
                    .map((_, index) => (
                      <LoadingBookCard key={`loading-recommended-${index}`} />
                    ))
                : recommendedBooks.map((book, index) => (
                    <BookCard
                      key={book.id || `recommended-${index}`}
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
