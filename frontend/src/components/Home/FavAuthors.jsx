import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const FavAuthors = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const selectedGenre = state?.selectedGenre || null;

  const handleRedirect = async () => {
    // Replace the endpoint with your actual backend URL
    const response = await axios.get(`http://localhost:1000/api/v1/initial-recommendations?genre=${selectedGenre}`);
    
    // Redirecting to the Authors page with the response data (if needed)
    navigate('/authors', { state: { recommendations: response.data } });
  };

  return (
    <div className="w-[1200px] mx-auto bg-zinc-900 h-auto lg:h-[89vh] flex flex-col px-10 py-8 lg:py-0">
      <h1 className="text-6xl font-semibold text-center my-5 text-yellow-100">Select your favorite genres</h1>
      {selectedGenre && (
        <div className="text-white text-xl text-center mb-5">
          Selected Genre: <span className="font-bold">{selectedGenre}</span>
        </div>
      )}
      {/* The rest of your genre selection */}
      <div className='flex text-center items-center justify-center w-100 my-5'>
        <div className="bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 genrecontinue text-center">
          <button className="px-5 py-2" onClick={handleRedirect}>Next</button>
        </div>
      </div>
    </div>
  );
};

export default FavAuthors;
