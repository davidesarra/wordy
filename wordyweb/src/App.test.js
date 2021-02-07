import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('renders wordy header', () => {
  const { getByText } = render(<App />);
  const element = getByText(/wordy/i);
  expect(element).toBeInTheDocument();
});
