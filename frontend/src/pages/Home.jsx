import { useEffect, useState } from "react";
import Hero from "../components/Home/Hero";
import RecentlyAdded from "../components/Home/RecentlyAdded";
import RecommendedBooks from "../components/Home/RecommendedBooks";
import FavAuthors from "../components/Home/FavAuthors";
import { useUser } from "@clerk/clerk-react";
import Carousel from "../components/Home/carousel";
import CarouselBooks from "../components/Home/CarouselBooks";

const Home = () => {
  const { isSignedIn, user } = useUser();
  const [isFirstLogin, setIsFirstLogin] = useState(false);

  useEffect(() => {
    window.scrollTo(0, 0);

    if (isSignedIn && user) {
      const firstLogin = localStorage.getItem(`firstLogin_${user.id}`);
      if (!firstLogin) {
        setIsFirstLogin(true);
        localStorage.setItem(`firstLogin_${user.id}`, 'true');
      }
    }
  }, [isSignedIn, user]);

  return (
    <>
      {!isSignedIn ? (
        <>
          <Hero />
          <RecommendedBooks />
          <RecentlyAdded />
        </>
      ) : (
        <>
          {isFirstLogin ? (
            <FavAuthors />
          ) : (
            <>
             <CarouselBooks />
              <Carousel />
            </>
          )}
        </>
      )}
    </>
  );
};

export default Home;
