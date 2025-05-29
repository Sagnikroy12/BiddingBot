import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch({
    headless: false,
    args: ['--start-maximized']
  });

  const context = await browser.newContext({
    viewport: null
  });

  const page = await context.newPage();
  await page.goto('https://www.eye2serve.com:9001/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html#Shell-home ');
// await page.goto('https://google.com')

//   await page.waitForSelector()
await page.locator("//input[@id='USERNAME_FIELD-inner']").fill('2209147') 
await page.locator("//input[@id='PASSWORD_FIELD-inner']").fill('Bs@2025')
await page.locator('//button[@id="LOGIN_LINK"]').click();

// await page.locator('//div[@id="__content6"]').click()

const [newpage] = await Promise.all([
  context.waitForEvent('page'),
  page.click('//div[@id="__content6"]')
]);

try {
    // await newpage.waitForSelector('#\\__mbox-btn-0', { timeout: 5000 });
    await newpage.click('#\\__mbox-btn-0');
    console.log('✅ Modal appeared and was dismissed.');
  } catch (e) {
    console.log('🕊️ No modal appeared within timeout.');
  }

await newpage.locator('//*[contains(text(),"Show Search")]').click()
await newpage.locator('//ul[@id="__list0"]').nth(1).click()
console.log('Ended')

console.log('Maximized and loaded:', await page.title());  
//   await page.close(); // Keep it open for debugging
})();

