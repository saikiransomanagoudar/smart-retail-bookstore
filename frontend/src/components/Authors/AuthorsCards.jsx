import React, { useState } from 'react';

const AuthorCards = () => {
  // State to track selected card indices
  const [selectedCards, setSelectedCards] = useState([]);

  // Function to toggle card selection
  const toggleSelection = (index) => {
    if (selectedCards.includes(index)) {
      setSelectedCards(selectedCards.filter((i) => i !== index));
    } else {
      setSelectedCards([...selectedCards, index]);
    }
  };

  // Author data
  const authors = [
    { name: 'William Shakespeare (1564-1616)', description: 'English playwright and poet', image: '/Authors/William-Shakespeare.jpg' },
    { name: 'Leo Tolstoy (1828-1910)', description: 'Russian novelist', image: '/Authors/Leo-Tolstoy.jpg' },
    { name: 'Charles Dickens (1812-1870)', description: 'English novelist', image: '/Authors/Charles-Dickens.jpg' },
    { name: 'Jane Austen (1775-1817)', description: 'English novelist', image: '/Authors/Jane-Austen.jpg' },
    { name: 'Mark Twain (1835-1910)', description: 'American author', image: '/Authors/Mark-Twain.jpg' },
    { name: 'Homer (c. 8th century BC)', description: 'Ancient Greek poet', image: '/Authors/Homer.jpg' },
    { name: 'F. Scott Fitzgerald (1896-1940)', description: 'American novelist', image: '/Authors/F-Scott-Fitzgerald.jpg' },
    { name: 'Gabriel García Márquez (1927-2014)', description: 'Colombian novelist', image: '/Authors/Gabriel-García-Márquez.jpg' },
    { name: 'Virginia Woolf (1882-1941)', description: 'English writer', image: '/Authors/Virginia-Woolf.jpg' },
    { name: 'George Orwell (1903-1950)', description: 'English novelist', image: '/Authors/George-Orwell.jpg' },
    { name: 'Ernest Hemingway (1899-1961)', description: 'American novelist', image: '/Authors/Ernest-Hemingway.jpg' },
    { name: 'Franz Kafka (1883-1924)', description: 'Czech writer', image: '/Authors/Franz-Kafka.jpg' },
    { name: 'James Joyce (1882-1941)', description: 'Irish novelist', image: '/Authors/James-Joyce.jpg' },
    { name: 'Haruki Murakami (1949-present)', description: 'Japanese author', image: '/Authors/Haruki-Murakami.jpg' },
    {
        "name": "Maya Angelou (1928-2014)",
        "description": "American poet",
        "image": "/Authors/Maya-Angelou.jpg"
      },
      {
        "name": "Toni Morrison (1931-2019)",
        "description": "American novelist",
        "image": "/Authors/Toni-Morrison.jpg"
      },
      {
        "name": "Mary Shelley (1797-1851)",
        "description": "English author",
        "image": "/Authors/Mary-Shelley.jpg"
      },
      {
        "name": "J.K. Rowling (1965-present)",
        "description": "British author",
        "image": "/Authors/J.K-Rowling.jpg"
      },
      {
        "name": "Chinua Achebe (1930-2013)",
        "description": "Nigerian novelist",
        "image": "/Authors/Chinua-Achebe.jpg"
      },
      {
        "name": "Ray Bradbury (1920-2012)",
        "description": "American author",
        "image": "/Authors/Ray-Bradbury.jpg"
      },
  ];

  return (
    <>
      <div className='bg-zinc-900 h-auto w-full flex flex-col lg:flex-col px-10 py-8 lg:py-0'>
      <h1 class="text-3xl font-semibold text-center my-5 text-yellow-100">Select your favorite Authors</h1>
     
    <div className="grid grid-cols-1 gap-6 md:grid-cols-3 w-[1200px] mx-auto my-6">
      {authors.map((author, index) => (
        <div
          key={index}
          onClick={() => toggleSelection(index)}
          className={`flex flex-col items-center space-x-4 p-4 shadow rounded-lg cursor-pointer ${
            selectedCards.includes(index) ? 'bg-gray-300' : 'bg-white'
          }`}
        >
          <img className="w-[4rem] h-[4rem] rounded-full" src={author.image} alt={`${author.name} Picture`} />
          <div className="text-center">
            <strong>{author.name}</strong> <br />
            <span>{author.description}</span>
          </div>
        </div>
      ))}
    </div>
    </div>
      </>
  );
};

export default AuthorCards;
