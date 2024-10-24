import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import '@fortawesome/fontawesome-free/css/all.min.css';



// Sample JSON Data (can be fetched from an API)
const movies = [
    { id: 1, title: "Khel Khel Mein", image: "/Authors/William-Shakespeare.jpg" },
    { id: 2, title: "Kandhal", image: "/Authors/Leo-Tolstoy.jpg" },
    { id: 3, title: "The Greatest of All Time", image: "/Authors/Charles-Dickens.jpg" },
    { id: 4, title: "Mathu Vadalara", image: "/Authors/Jane-Austen.jpg" },
    { id: 5, title: "CTRL", image: "/Authors/Mark-Twain.jpg" },
    { id: 1, title: "Khel Khel Mein", image: "/Authors/William-Shakespeare.jpg" },
    { id: 2, title: "Kandhal", image: "/Authors/Leo-Tolstoy.jpg" },
    { id: 3, title: "The Greatest of All Time", image: "/Authors/Charles-Dickens.jpg" },
    { id: 4, title: "Mathu Vadalara", image: "/Authors/Jane-Austen.jpg" },
    { id: 5, title: "CTRL", image: "/Authors/Mark-Twain.jpg" },
    { id: 1, title: "Khel Khel Mein", image: "/Authors/William-Shakespeare.jpg" },
    { id: 2, title: "Kandhal", image: "/Authors/Leo-Tolstoy.jpg" },
    { id: 3, title: "The Greatest of All Time", image: "/Authors/Charles-Dickens.jpg" },
    { id: 4, title: "Mathu Vadalara", image: "/Authors/Jane-Austen.jpg" },
    { id: 5, title: "CTRL", image: "/Authors/Mark-Twain.jpg" },
  ];

const Carousel = () => {
  const settings = {
    dots: false,
    infinite: true,
    speed: 500,
    slidesToShow: 5,
    slidesToScroll: 1,
    nextArrow: <SampleNextArrow />,
    prevArrow: <SamplePrevArrow />,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 5,
        },
      },
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 3,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
        },
      },
    ],
  };

  // Custom Next Arrow
  function SampleNextArrow(props) {
    const { onClick } = props;
    return (
      <div
        className="absolute top-1/2 right-0 transform -translate-y-1/2 z-10 cursor-pointer bg-zinc-800 -right-5"
        onClick={onClick}
      >
        <button className="h-16 px-1">
           <i className="fas fa-chevron-right text-white text-2xl"></i>
        </button>
        
      </div>
    );
  }

  // Custom Previous Arrow
  function SamplePrevArrow(props) {
    const { onClick } = props;
    return (
      <div
        className="absolute top-1/2 left-0 transform -translate-y-1/2 z-10 cursor-pointer bg-zinc-800 -left-5"
        onClick={onClick}
      >
        <button className="h-16 px-1">
           <i className="fas fa-chevron-left text-white text-2xl"></i>
        </button>
      </div>
    );
  }

  return (
    <>
    <div className="bg-zinc-900">
    <div className="mx-auto  flex flex-col px-10 py-8 lg:py-0">
    <div>
    <h1 className="text-3xl font-semibold text-left my-5 text-yellow-100">Authors Who Shaped</h1>
    </div>
    
    <div className="relative w-full p-8">
      <Slider {...settings}>
        {/* Iterating over JSON data */}
        {movies.map((movie) => (
          <div key={movie.id} className="px-2">
            <div className="bg-gray-800 text-white p-4 rounded-lg">
              <img
                src={movie.image}
                alt={movie.title}
                className="rounded-lg mb-2 w-[15.25rem] h-[12.75rem] object-cover"
              />
              <h2 className="text-lg font-semibold text-center">{movie.title}</h2>
              <p className="text-red-500">{movie.status}</p>
            </div>
          </div>
        ))}
      </Slider>
    </div>
    </div>
    </div>
    </>
  );
};

export default Carousel;
