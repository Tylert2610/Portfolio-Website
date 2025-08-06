import React from 'react';

const TailwindTest: React.FC = () => {
  return (
    <div className="p-8 max-w-md mx-auto mt-8">
      <div className="bg-white rounded-lg shadow-lg p-6 border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Tailwind CSS Test
        </h2>

        {/* Colors */}
        <div className="space-y-2 mb-4">
          <div className="h-8 bg-red-500 rounded flex items-center justify-center text-white font-semibold">
            Red Background
          </div>
          <div className="h-8 bg-green-500 rounded flex items-center justify-center text-white font-semibold">
            Green Background
          </div>
          <div className="h-8 bg-blue-500 rounded flex items-center justify-center text-white font-semibold">
            Blue Background
          </div>
        </div>

        {/* Typography */}
        <div className="space-y-2 mb-4">
          <p className="text-sm text-gray-600">Small text</p>
          <p className="text-base text-gray-700">Base text</p>
          <p className="text-lg font-semibold text-gray-800">Large bold text</p>
        </div>

        {/* Spacing and Layout */}
        <div className="space-y-2 mb-4">
          <div className="flex space-x-2">
            <div className="w-4 h-4 bg-yellow-400 rounded"></div>
            <div className="w-4 h-4 bg-yellow-400 rounded"></div>
            <div className="w-4 h-4 bg-yellow-400 rounded"></div>
          </div>
        </div>

        {/* Responsive Design */}
        <div className="text-center">
          <p className="text-xs sm:text-sm md:text-base lg:text-lg xl:text-xl text-purple-600">
            Responsive text (resize window to test)
          </p>
        </div>

        {/* Hover Effects */}
        <button className="w-full mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded transition-colors duration-200">
          Hover me!
        </button>

        {/* Status Indicator */}
        <div className="mt-4 p-3 bg-green-100 border border-green-400 rounded">
          <p className="text-green-800 text-sm">
            ✅ If you can see all the colored boxes, styled text, and hover
            effects, Tailwind CSS is working correctly!
          </p>
        </div>
      </div>
    </div>
  );
};

export default TailwindTest;
