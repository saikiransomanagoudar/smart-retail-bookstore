import { SignUp, useUser } from "@clerk/clerk-react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const { isSignedIn } = useUser();
  const navigate = useNavigate();

  useEffect(() => {
    if (isSignedIn) {
      navigate("/");
    }
  }, [isSignedIn, navigate]);

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-blue-500 via-green-500 to-teal-500">
      <div className="w-full max-w-md">
        <SignUp
          path="/signup"
          routing="path"
          signInUrl="/login"
          appearance={{
            elements: {
              card: "bg-white shadow-lg rounded-lg text-gray-700 p-6",
              input: "border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 rounded-lg",
              button: "bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-lg transition-all duration-300",
            },
          }}
        />
      </div>
    </div>
  );
};

export default Signup;
