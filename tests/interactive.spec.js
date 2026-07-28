const { test, expect } = require("@playwright/test");

test("fresh browser starts a playable game and accepts rotation", async ({ page }) => {
  await page.goto(process.env.ATO_APP_URL || "http://127.0.0.1:8080/");
  await expect(page.locator("#canvas")).toBeVisible();
  await expect(page.locator("#pauseBtn")).toBeVisible();
  await expect(page.locator("#gameoverscreen")).toBeHidden();

  await expect(page.locator("body")).toHaveAttribute("data-ato-game-state", "1");

  const before = await page.locator("body").getAttribute("data-ato-position");
  await page.keyboard.press("ArrowRight");
  await expect(page.locator("body")).toHaveAttribute("data-ato-rotations", "1");
  await expect(page.locator("body")).not.toHaveAttribute("data-ato-position", before);

  await page.keyboard.down("ArrowDown");
  await expect
    .poll(async () => Number(await page.locator("body").getAttribute("data-ato-block-count")), {
      timeout: 10_000,
    })
    .toBeGreaterThan(0);
  await page.keyboard.up("ArrowDown");
});
