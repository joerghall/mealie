import { describe, expect, test } from "vitest";
import { calculateRecipeDimensionScale } from "../use-recipe-dimension-scaling";

describe("calculateRecipeDimensionScale", () => {
  test("scales a round recipe by diameter squared", () => {
    expect(calculateRecipeDimensionScale({
      basis: "round",
      baseLength: 10,
      targetLength: 12,
    })).toBeCloseTo(1.44);
  });

  test("scales a square recipe by side squared", () => {
    expect(calculateRecipeDimensionScale({
      basis: "square",
      baseLength: 20,
      targetLength: 30,
    })).toBeCloseTo(2.25);
  });

  test("scales a rectangular recipe by area", () => {
    expect(calculateRecipeDimensionScale({
      basis: "rectangle",
      baseLength: 20,
      baseWidth: 10,
      targetLength: 30,
      targetWidth: 15,
    })).toBeCloseTo(2.25);
  });

  test("returns the neutral scale for invalid dimensions", () => {
    expect(calculateRecipeDimensionScale({
      basis: "rectangle",
      baseLength: 20,
      baseWidth: 0,
      targetLength: 30,
      targetWidth: 15,
    })).toBe(1);
  });
});
