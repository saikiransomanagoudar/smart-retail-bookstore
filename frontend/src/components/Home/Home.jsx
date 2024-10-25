import { useNavigate } from "react-router-dom";
import { useUser } from "@clerk/clerk-react";
import { useState } from "react";
import { Search, ChevronRight, BookOpen, Star, Users } from "lucide-react"; // Import icons

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="bg-zinc-800/50 backdrop-blur-sm p-6 rounded-xl border border-zinc-700 hover:border-yellow-100/30 transition-all duration-300 hover:transform hover:-translate-y-1">
    <div className="flex items-center space-x-4">
      <div className="p-3 bg-yellow-100/10 rounded-lg">
        <Icon className="w-6 h-6 text-yellow-100" />
      </div>
      <div>
        <h3 className="text-yellow-100 font-semibold text-lg">{title}</h3>
        <p className="text-zinc-400 text-sm mt-1">{description}</p>
      </div>
    </div>
  </div>
);

const Hero = () => {
  const { isSignedIn } = useUser();
  const navigate = useNavigate();
  const [showGenreModal, setShowGenreModal] = useState(false);
  const [setSelectedGenres] = useState([]);
  const [isSearchFocused, setIsSearchFocused] = useState(false);

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
    <div className="relative min-h-screen bg-gradient-to-br from-zinc-900 via-zinc-900 to-zinc-800 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxjaXJjbGUgZmlsbD0icmdiYSgyNTUsIDI1NSwgMjU1LCAwLjAyKSIgY3g9IjMwIiBjeT0iMzAiIHI9IjMwIi8+PC9nPjwvc3ZnPg==')] opacity-20" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl lg:text-7xl font-bold text-white">
                <span className="text-yellow-100">Discover</span> Your Next Great Read
              </h1>
              <p className="text-xl text-zinc-300 max-w-lg">
                Experience personalized book recommendations powered by AI. Find your perfect match from thousands of titles.
              </p>
            </div>


            {/* CTA Button */}
            <button
              onClick={handleDiscoverBooksClick}
              className="group bg-gradient-to-r from-yellow-100 to-yellow-200 text-zinc-900 rounded-full py-4 px-8 text-lg font-semibold hover:from-yellow-200 hover:to-yellow-300 transition-all duration-300 flex items-center space-x-2"
            >
              <span>Start Your Journey</span>
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" />
            </button>

            {/* Features Grid */}
            <div className="grid sm:grid-cols-2 gap-4 mt-12">
              <FeatureCard
                icon={BookOpen}
                title="Vast Library"
                description="Access thousands of books across all genres"
              />
              <FeatureCard
                icon={Star}
                title="Smart Recommendations"
                description="AI-powered suggestions based on your preferences"
              />
            </div>
          </div>

          {/* Right Column - Image */}
          <div className="relative lg:h-[800px] flex items-center justify-center">
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-yellow-100/20 rounded-full blur-3xl" />
            <img
              src="/hero.png"
              alt="Books collection"
              className="relative w-full h-auto max-w-2xl object-contain drop-shadow-2xl transform hover:scale-105 transition-transform duration-500"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;