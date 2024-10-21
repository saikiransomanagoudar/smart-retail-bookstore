import React from 'react';
import { useNavigate } from 'react-router-dom';


const FavAuthors = () => {

    const navigate = useNavigate();

    const handleRedirect = () => {
        navigate('/Authors'); // Replace with your target route
    };

    return (
      <>
      <div className="w-[1200px] mx-auto bg-zinc-900 h-auto lg:h-[89vh] w-full flex flex-col lg:flex-col px-10 py-8 lg:py-0">
        <h1 class="text-6xl font-semibold text-center my-5 text-yellow-100">Select your favorite genres</h1>
        <div className="genres_form flex flex-wrap gap-2.5 mt-5">
          <div className="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Art">
            <label className="flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
              <input type="hidden" name="favorites[Art]" value="false" />
              <input className='pt-2' type="checkbox" name="favorites[Art]" id="favorites_Art" value="true" />
              Art
            </label>
          </div>
          <div className="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Biography">
            <label className="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
              <input type="hidden" name="favorites[Biography]" value="false" />
              <input type="checkbox" name="favorites[Biography]" id="favorites_Biography" value="true" />
              Biography
            </label>
          </div>
          <div className="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Chick-lit">
          <label className="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Chick-lit]" id="" value="false" />
            <input type="checkbox" name="favorites[Chick-lit]" id="favorites_Chick-lit" value="true" />
            Chick Lit
         </label>
         </div>
         <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Children's">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Children's]" id="" value="false" />
            <input type="checkbox" name="favorites[Children's]" id="favorites_Children_s" value="true" />
            Children's
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Christian">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Christian]" id="" value="false" />
            <input type="checkbox" name="favorites[Christian]" id="favorites_Christian" value="true" />
            Christian
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Classics">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Classics]" id="" value="false" />
            <input type="checkbox" name="favorites[Classics]" id="favorites_Classics" value="true" />
            Classics
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Comics">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Comics]" id="" value="false" />
            <input type="checkbox" name="favorites[Comics]" id="favorites_Comics" value="true" />
            Comics
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Contemporary">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Contemporary]" id="" value="false" />
            <input type="checkbox" name="favorites[Contemporary]" id="favorites_Contemporary" value="true" />
            Contemporary
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Cookbooks">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Cookbooks]" id="" value="false" />
            <input type="checkbox" name="favorites[Cookbooks]" id="favorites_Cookbooks" value="true" />
            Cookbooks
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Crime">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Crime]" id="" value="false" />
            <input type="checkbox" name="favorites[Crime]" id="favorites_Crime" value="true" />
            Crime
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Ebooks">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Ebooks]" id="" value="false" />
            <input type="checkbox" name="favorites[Ebooks]" id="favorites_Ebooks" value="true" />
            Ebooks
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Fantasy">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Fantasy]" id="" value="false" />
            <input type="checkbox" name="favorites[Fantasy]" id="favorites_Fantasy" value="true" />
            Fantasy
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Fiction">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Fiction]" id="" value="false" />
            <input type="checkbox" name="favorites[Fiction]" id="favorites_Fiction" value="true" />
            Fiction
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Gay and Lesbian">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Gay and Lesbian]" id="" value="false" />
            <input type="checkbox" name="favorites[Gay and Lesbian]" id="favorites_Gay_and_Lesbian" value="true" />
            Gay and Lesbian
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Graphic novels">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Graphic novels]" id="" value="false" />
            <input type="checkbox" name="favorites[Graphic novels]" id="favorites_Graphic_novels" value="true" />
            Graphic Novels
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Historical fiction">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Historical fiction]" id="" value="false" />
            <input type="checkbox" name="favorites[Historical fiction]" id="favorites_Historical_fiction" value="true" />
            Historical Fiction
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_History">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[History]" id="" value="false" />
            <input type="checkbox" name="favorites[History]" id="favorites_History" value="true" />
            History
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Horror">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Horror]" id="" value="false" />
            <input type="checkbox" name="favorites[Horror]" id="favorites_Horror" value="true" />
            Horror
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Humor and Comedy">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Humor and Comedy]" id="" value="false" />
            <input type="checkbox" name="favorites[Humor and Comedy]" id="favorites_Humor_and_Comedy" value="true" />
            Humor and Comedy
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Manga">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Manga]" id="" value="false" />
            <input type="checkbox" name="favorites[Manga]" id="favorites_Manga" value="true" />
            Manga
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Memoir">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Memoir]" id="" value="false" />
            <input type="checkbox" name="favorites[Memoir]" id="favorites_Memoir" value="true" />
            Memoir
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Music">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Music]" id="" value="false" />
            <input type="checkbox" name="favorites[Music]" id="favorites_Music" value="true" />
            Music
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Mystery">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Mystery]" id="" value="false" />
            <input type="checkbox" name="favorites[Mystery]" id="favorites_Mystery" value="true" />
            Mystery
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Non-fiction">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Non-fiction]" id="" value="false" />
            <input type="checkbox" name="favorites[Non-fiction]" id="favorites_Non-fiction" value="true" />
            Nonfiction
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Paranormal">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Paranormal]" id="" value="false" />
            <input type="checkbox" name="favorites[Paranormal]" id="favorites_Paranormal" value="true" />
            Paranormal
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Philosophy">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Philosophy]" id="" value="false" />
            <input type="checkbox" name="favorites[Philosophy]" id="favorites_Philosophy" value="true" />
            Philosophy
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Poetry">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Poetry]" id="" value="false" />
            <input type="checkbox" name="favorites[Poetry]" id="favorites_Poetry" value="true" />
            Poetry
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Psychology">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Psychology]" id="" value="false" />
            <input type="checkbox" name="favorites[Psychology]" id="favorites_Psychology" value="true" />
            Psychology
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Religion">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Religion]" id="" value="false" />
            <input type="checkbox" name="favorites[Religion]" id="favorites_Religion" value="true" />
            Religion
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Romance">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Romance]" id="" value="false" />
            <input type="checkbox" name="favorites[Romance]" id="favorites_Romance" value="true" />
            Romance
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Science">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Science]" id="" value="false" />
            <input type="checkbox" name="favorites[Science]" id="favorites_Science" value="true" />
            Science
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Science fiction">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Science fiction]" id="" value="false" />
            <input type="checkbox" name="favorites[Science fiction]" id="favorites_Science_fiction" value="true" />
            Science Fiction
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Self help">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Self help]" id="" value="false" />
            <input type="checkbox" name="favorites[Self help]" id="favorites_Self_help" value="true" />
            Self Help
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Suspense">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Suspense]" id="" value="false" />
            <input type="checkbox" name="favorites[Suspense]" id="favorites_Suspense" value="true" />
            Suspense
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Spirituality">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Spirituality]" id="" value="false" />
            <input type="checkbox" name="favorites[Spirituality]" id="favorites_Spirituality" value="true" />
            Spirituality
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Sports">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Sports]" id="" value="false" />
            <input type="checkbox" name="favorites[Sports]" id="favorites_Sports" value="true" />
            Sports
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Thriller">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Thriller]" id="" value="false" />
            <input type="checkbox" name="favorites[Thriller]" id="favorites_Thriller" value="true" />
            Thriller
            </label>
            </div>
            <div class="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Travel">
            <label class="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
            <input type="hidden" name="favorites[Travel]" id="" value="false" />
            <input type="checkbox" name="favorites[Travel]" id="favorites_Travel" value="true" />
            Travel
            </label>
            </div>
          <div className="genreButton bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 hover:bg-zinc-800 transition-all duration-300" id="genre_Young-adult">
            <label className="genreLabel flex items-center justify-center genreLabel inline-block align-middle font-sans overflow-hidden px-2.5 py-1.5 text-ellipsis whitespace-nowrap w-64">
              <input type="hidden" name="favorites[Young_adult]" value="false" />
              <input type="checkbox" name="favorites[Young_adult]" id="favorites_Young_adult" value="true" />
              Young Adult
            </label>
          </div>
        </div>
        <div className='flex text-center items-center justify-center w-100 my-5'>
        <div className="bg-zinc-900 rounded-full text-2xl flex w-64 items-center justify-center text-white font-semibold border border-yellow-100 genrecontinue text-center">
           <button className="px-5 py-2" onClick={handleRedirect}>Next</button>
          </div>
          </div>
        </div>
      </>
    );
  };
  
  export default FavAuthors;
  