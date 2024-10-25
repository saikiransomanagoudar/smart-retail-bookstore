import { useNavigate } from "react-router-dom";
import { useUser } from "@clerk/clerk-react";
import { useState } from "react";

const Hero = () => {
  const { isSignedIn } = useUser();
  const navigate = useNavigate();

  const [showGenreModal, setShowGenreModal] = useState(false);
  const [setSelectedGenres] = useState([]);

  const handleDiscoverBooksClick = () => {
    if (!isSignedIn) {
      navigate("/login");
    } else {
      setShowGenreModal(true);
    }
  };

  const handleGenreNext = (genres) => {
    setSelectedGenres(genres);
    setShowGenreModal(false);
  };

  return (
    <div className="bg-zinc-900 h-auto lg:h-[89vh] w-full flex flex-col lg:flex-row px-10 py-8 lg:py-0">
      <div className="w-full lg:w-3/6 h-[100%] flex items-center justify-center">
        <div className="w-full">
          <h1 className="text-yellow-100 text-6xl font-semibold text-center lg:text-left">
            Discover Your Next Great Read
          </h1>
          <p className='text-xl text-zinc-300 mt-5 text-center lg:text-left'>
            Revolutionizing Book Shopping with AI-Powered Recommendations
          </p>
          <div className="flex justify-center lg:justify-start">
            <button
              onClick={handleDiscoverBooksClick}
              className="my-5 lg:my-8 text-3xl bg-zinc-900 rounded-full py-3 px-8 flex items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300"
            >
              Discover Books
            </button>
          </div>
        </div>
      </div>
      <div className="w-full lg:w-3/6 h-auto lg:h-[100%] flex items-center justify-center">
        <img
          src="/hero.png"
          alt="hero"
          className="h-auto lg:h-[100%] object-cover"
        />
      </div>
    </div>
  );
};

export default Hero;
