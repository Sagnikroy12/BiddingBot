import { chromium, Page } from 'playwright';

(async () => {
  const browser = await chromium.launch({ headless: false, args: ['--start-maximized'] });
  const context = await browser.newContext({
    viewport: null, // Use full screen
  });
  const page = await context.newPage();

  // 1. Open the link
  await page.goto('https://www.eye2serve.com:9001/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html#Shell-home'); // Replace with actual URL

  // 2. Perform login
  await page.fill('//input[@id="USERNAME_FIELD-inner"]', '2209147'); // Replace with actual selector and username
  await page.fill('//input[@id="PASSWORD_FIELD-inner"]', 'Bs@2025'); // Replace with actual selector and password
  await page.click('//button[@id="LOGIN_LINK"]'); // Replace with actual selector

  // 3. Wait for navigation after login (if needed)
  await page.waitForNavigation();

  // 4. Click on something that opens a new tab
  const [newPage] = await Promise.all([
    context.waitForEvent('page'),
    page.click('//div[@id="__content6"]'), // Replace with actual selector
  ]);

  try{
    await newPage.click('#\\__mbox-btn-0');
    console.log('Clicked on the button in the new tab');
  }catch (error) {
    console.error('No button appeared');
  }

  await newPage.locator('//*contains(text(), "Show Search")').click(); // Replace with actual selector for the "Bid" link
  await newPage.locator('//ul[@id="__list0"]/li[1]').click(); // Replace with actual selector for the first bid
  await newPage.locator('//button[@id="__button3"]').click(); // Replace with actual selector for the "Bid" button

  const destination = "//table//tr[ROW_INDEX]/td[4]"; // Replace with actual selector for the destination column
  const spi = "//table//tr[ROW_INDEX]/td[11]"
  const freight = "//table//tr[ROW_INDEX]/td[12]"
  const bid = "//table//tr[ROW_INDEX]/td[13]"
  console.log('Ended')
  // Close browser when done
  // await browser.close();
})();