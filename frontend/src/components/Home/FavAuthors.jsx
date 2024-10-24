import React from 'react';
import { useNavigate } from 'react-router-dom';

// Dummy JSON data for genres
const genresData = [
  { id: 'Art', label: 'Art' },
  { id: 'Biography', label: 'Biography' },
  { id: 'Chick-lit', label: 'Chick Lit' },
  { id: "Children's", label: "Children's" },
  { id: 'Christian', label: 'Christian' },
  { id: 'Classics', label: 'Classics' },
  { id: 'Comics', label: 'Comics' },
  { id: 'Contemporary', label: 'Contemporary' },
  { id: 'Historical fiction', label: 'Historical Fiction' },
  { id: 'History', label: 'History' },
  { id: 'Horror', label: 'Horror' },
  { id: 'Humor and Comedy', label: 'Humor and Comedy' },
  { id: 'Manga', label: 'Manga' },
  { id: 'Memoir', label: 'Memoir' },
  { id: 'Non-fiction', label: 'Nonfiction' },
  { id: 'Paranormal', label: 'Paranormal' },
  { id: 'Philosophy', label: 'Philosophy' },
  { id: 'Poetry', label: 'Poetry' },
  { id: 'Psychology', label: 'Psychology' },
  { id: 'Religion', label: 'Religion' },
  { id: 'Romance', label: 'Romance' },
  { id: 'Science', label: 'Science' },
  { id: 'Science fiction', label: 'Science Fiction' },
  { id: 'Self help', label: 'Self Help' },
  { id: 'Suspense', label: 'Suspense' },
  { id: 'Spirituality', label: 'Spirituality' },
  { id: 'Sports', label: 'Sports' },
  { id: 'Thriller', label: 'Thriller' },
  { id: 'Travel', label: 'Travel' },
  { id: 'Young-adult', label: 'Young Adult' },
];

const FavAuthors = () => {
  const navigate = useNavigate();

  const handleRedirect = () => {
    navigate('/Authors'); // Replace with your target route
  };

  return (
    <div className="w-[1200px] mx-auto bg-zinc-900 h-auto lg:h-[89vh] flex flex-col px-10 py-8 lg:py-0">
      <h1 className="text-6xl font-semibold text-center my-5 text-yellow-100">Select your favorite genres</h1>
      <div className="genres_form flex flex-wrap gap-2.5 mt-5">
        {genresData.map((genre) => (
          <div key={genre.id} className="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300">
            <label className="flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
              <input type="hidden" name={`favorites[${genre.id}]`} value="false" />
              <input className='mr-2' type="checkbox" name={`favorites[${genre.id}]`} id={`favorites_${genre.id}`} value="true" />
              {genre.label}
            </label>
          </div>
        ))}
      </div>
      <div className='flex text-center items-center justify-center w-100 my-5'>
        <div className="bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 genrecontinue text-center">
          <button className="px-5 py-2" onClick={handleRedirect}>Next</button>
        </div>
      </div>
    </div>
  );
};

export default FavAuthors;
