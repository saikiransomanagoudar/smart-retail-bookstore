import { useEffect, useState } from "react";
import Hero from "../components/Home/Hero";
import RecentlyAdded from "../components/Home/RecentlyAdded";
import RecommendedBooks from "../components/Home/RecommendedBooks";
import FavAuthors from "../components/Home/FavAuthors";
import { useUser } from "@clerk/clerk-react";
import Carousel from "../components/Home/carousel";
import CarouselBooks from "../components/Home/CarouselBooks";
import MoreInCrime from "../components/Home/MoreInCrime";
import MoreInMystery from "../components/Home/MoreInMystery";
import MoreInRowling from "../components/Home/MoreRowling";

const Home = () => {
  const { isSignedIn, user } = useUser(); // Retrieve user info from Clerk
  const [isFirstLogin, setIsFirstLogin] = useState(false);

  useEffect(() => {
    window.scrollTo(0, 0);

    if (isSignedIn && user) {
      // Example: Check if it's the user's first login (you can replace this with your logic)
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
            <FavAuthors /> // Show favorite authors if it's the first login
          ) : (
            <>
              <MoreInCrime />
              <MoreInMystery />
              <MoreInRowling />
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
