import { render, screen } from '@testing-library/react';
import RegistrationPage from './RegistrationPage';

test('renders learn react link', () => {
  render(<RegistrationPage />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
