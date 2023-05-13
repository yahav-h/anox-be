import { render, screen } from '@testing-library/react';
import DashboardPage from "./DashboardPage";

test('renders learn react link', () => {
  render(<DashboardPage />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
