import React, { useEffect } from "react";
import Hero from "../components/Home/Hero";
import RecentlyAdded from "../components/Home/RecentlyAdded";
import Chatbot from "../components/Chatbot/Chatbot";

const Home = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <>
      <Hero />
      <RecentlyAdded />
      <Chatbot />
    </>
  );
};

export default Home;
