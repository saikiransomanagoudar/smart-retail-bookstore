import { useEffect } from "react";
import Hero from "../components/Home/Hero";
import RecentlyAdded from "../components/Home/RecentlyAdded";
import RecommendedBooks from "../components/Home/RecommendedBooks";
const Home = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <>
      <Hero />
      <RecommendedBooks />
      <RecentlyAdded />
    </>
  );
};

export default Home;
