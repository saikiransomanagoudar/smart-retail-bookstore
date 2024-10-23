import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import '@fortawesome/fontawesome-free/css/all.min.css';


const Books = [
    { id: 'Art', label: 'Art', image: "/Authors/William-Shakespeare.jpg"},
    { id: 'Biography', label: 'Biography', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Chick-lit', label: 'Chick Lit', image: "/Authors/William-Shakespeare.jpg" },
    { id: "Children's", label: "Children's", image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Christian', label: 'Christian', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Classics', label: 'Classics', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Comics', label: 'Comics', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Contemporary', label: 'Contemporary', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Historical fiction', label: 'Historical Fiction', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'History', label: 'History', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Horror', label: 'Horror', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Humor and Comedy', label: 'Humor and Comedy', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Manga', label: 'Manga', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Memoir', label: 'Memoir', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Non-fiction', label: 'Nonfiction', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Paranormal', label: 'Paranormal', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Philosophy', label: 'Philosophy', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Poetry', label: 'Poetry', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Psychology', label: 'Psychology', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Religion', label: 'Religion', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Romance', label: 'Romance', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Science', label: 'Science', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Science fiction', label: 'Science Fiction', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Self help', label: 'Self Help', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Suspense', label: 'Suspense', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Spirituality', label: 'Spirituality',image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Sports', label: 'Sports', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Thriller', label: 'Thriller', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Travel', label: 'Travel', image: "/Authors/William-Shakespeare.jpg" },
    { id: 'Young-adult', label: 'Young Adult', image: "/Authors/William-Shakespeare.jpg" },
  ];


const CarouselBooks = () => {
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
    <h1 className="text-6xl font-semibold text-center my-5 text-yellow-100">Favorite Books</h1>
    </div>
    
    <div className="relative w-full p-8">
      <Slider {...settings}>
        {/* Iterating over JSON data */}
        {Books.map((book) => (
          <div key={book.id} className="px-2">
            <div className="bg-gray-800 text-white p-4 rounded-lg">
              <img
                src={book.image}
                alt={book.label}
                className="rounded-lg mb-2"
              />
              <h2 className="text-lg font-semibold">{book.label}</h2>
              <p className="text-red-500">{book.status}</p>
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

export default CarouselBooks;
