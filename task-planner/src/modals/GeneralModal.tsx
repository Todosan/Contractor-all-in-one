import React from 'react';

interface GeneralModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

const GeneralModal: React.FC<GeneralModalProps> = ({ isOpen, onClose, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="relative bg-white p-6 rounded-md w-96">
        <button
          onClick={onClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        >
          ✖
        </button>
        <div>{children}</div>
      </div>
    </div>
  );
};

export default GeneralModal;
