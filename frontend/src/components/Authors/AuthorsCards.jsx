import React from 'react';
import { useNavigate } from 'react-router-dom';


const AuthorsCards = () => {


    return (
      <>
      <div className='bg-zinc-900 h-auto w-full flex flex-col lg:flex-col px-10 py-8 lg:py-0'>
      <h1 class="text-6xl font-semibold text-center my-5 text-yellow-100">Select your favorite Authors</h1>
      <div className="grid grid-cols-1 gap-6 md:grid-cols-3 w-[1200px] mx-auto my-6">
      <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/William-Shakespeare.jpg" alt="Profile Picture" />
        <div className="text-center">
            <strong>William Shakespeare (1564-1616)</strong> <br />
            <span>English playwright and poet</span>
        </div>
        </div>
      
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Leo-Tolstoy.jpg" />
        <div className="text-center">
            <strong>Leo Tolstoy (1828-1910)</strong> <br />
            <span>Russian novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Charles-Dickens.jpg" />
        <div className="text-center">
            <strong>Charles Dickens (1812-1870) </strong> <br />
            <span>English novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Jane-Austen.jpg" />
        <div className="text-center">
            <strong>Jane Austen (1775-1817)</strong> <br />
            <span>English novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Mark-Twain.jpg" />
        <div className="text-center">
            <strong>Mark Twain (1835-1910)</strong> <br />
            <span>American author</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Homer.jpg" />
        <div className="text-center">
        <strong>Homer (c. 8th century BC)</strong> <br />
        <span>Ancient Greek poet</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/F-Scott-Fitzgerald.jpg" />
        <div className="text-center">
        <strong>F. Scott Fitzgerald (1896-1940)</strong> <br />
        <span>American novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Gabriel-García-Márquez.jpg" />
        <div className="text-center">
        <strong>Gabriel García Márquez (1927-2014)</strong> <br />
        <span>Colombian novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Virginia-Woolf.jpg" />
        <div className="text-center">
        <strong>Virginia Woolf (1882-1941)</strong> <br />
        <span>English writer</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/George-Orwell.jpg" />
        <div className="text-center">
        <strong>George Orwell (1903-1950)</strong> <br />
        <span>English novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Ernest-Hemingway.jpg" />
        <div className="text-center">
        <strong>Ernest Hemingway (1899-1961)</strong> <br />
        <span>American novelist </span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Franz-Kafka.jpg" />
        <div className="text-center">
        <strong>Franz Kafka (1883-1924)</strong> <br />
        <span>Czech writer</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/James-Joyce.jpg" />
        <div className="text-center">
        <strong>James Joyce (1882-1941)</strong> <br />
        <span>Irish novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Haruki-Murakami.jpg" />
        <div className="text-center">
        <strong>Haruki Murakami (1949-present)</strong> <br />
        <span>Japanese author</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Maya-Angelou.jpg" />
        <div className="text-center">
        <strong>Maya Angelou (1928-2014)</strong> <br />
        <span>American poet</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Toni-Morrison.jpg" />
        <div className="text-center">
        <strong>Toni Morrison (1931-2019)</strong> <br />
        <span>American novelist</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Mary-Shelley.jpg" />
        <div className="text-center">
        <strong>Mary Shelley (1797-1851)</strong> <br />
        <span>English author</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/J.K-Rowling.jpg" />
        <div className="text-center">
        <strong>J.K. Rowling (1965-present)</strong> <br />
        <span>British author</span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Chinua-Achebe.jpg" />
        <div className="text-center">
        <strong>Chinua Achebe (1930-2013)</strong> <br />
        <span>Nigerian novelist </span>
        </div>
        </div>
        <div className="flex flex-col items-center space-x-4 p-4 bg-white shadow rounded-lg">
        <img className="w-12 h-12 rounded-full" src="/Authors/Ray-Bradbury.jpg" />
        <div className="text-center">
        <strong>Ray Bradbury (1920-2012)</strong> <br />
        <span>American author</span>
        </div>
        </div>
        
        </div>
        </div>
      </>
    );
  };
  
  export default AuthorsCards;
  

