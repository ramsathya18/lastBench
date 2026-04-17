import { render, screen } from "@testing-library/react";
import { Card } from "./ui";

describe("Card", () => {
  it("renders content", () => {
    render(<Card>hello</Card>);
    expect(screen.getByText("hello")).toBeInTheDocument();
  });
});
