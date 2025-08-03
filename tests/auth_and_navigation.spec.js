//Playwright  ----- End-to-End (E2E) UI Automation Testingconst 



const { test, expect } = require('@playwright/test');

const baseURL = 'http://localhost:5000'; // Adjust port if needed

test.describe('AbilityHire Web App Thorough UI Tests', () => {

    test('Sign in as Job Publisher', async({ page }) => {
        await page.goto(baseURL + '/login');
        await page.fill('input[name="email"]', 'publisher@example.com'); // Use valid test publisher email
        await page.fill('input[name="password"]', 'PublisherPass123!'); // Use valid test publisher password
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(baseURL + '/publisherdashboard');
        await expect(page.locator('text=Publisher Dashboard')).toBeVisible();
    });

    test('Sign in as Job Seeker', async({ page }) => {
        await page.goto(baseURL + '/login');
        await page.fill('input[name="email"]', 'seeker@example.com'); // Use valid test seeker email
        await page.fill('input[name="password"]', 'SeekerPass123!'); // Use valid test seeker password
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(baseURL + '/seekerdashboard');
        await expect(page.locator('text=Seeker Dashboard')).toBeVisible();
    });

    test('Sign up as Publisher', async({ page }) => {
        await page.goto(baseURL + '/signup');
        await page.fill('input[name="firstName"]', 'Test');
        await page.fill('input[name="lastName"]', 'Publisher');
        await page.fill('input[name="email"]', 'newpublisher@example.com');
        await page.fill('input[name="password"]', 'NewPublisherPass123!');
        await page.fill('input[name="repeatPassword"]', 'NewPublisherPass123!');
        await page.selectOption('select[name="role"]', 'publisher');
        await page.click('button[type="submit"]');
        // Fill publisher info form
        await expect(page).toHaveURL(baseURL + '/publisherinfo');
        await page.fill('input[name="phone"]', '1234567890');
        await page.fill('input[name="address"]', '123 Publisher St');
        await page.fill('input[name="city"]', 'PublisherCity');
        await page.fill('input[name="country"]', 'PublisherCountry');
        await page.selectOption('select[name="gender"]', 'Other');
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(baseURL + '/publisherdashboard');
        await expect(page.locator('text=Publisher Dashboard')).toBeVisible();
    });

    test('Sign up as Seeker', async({ page }) => {
        await page.goto(baseURL + '/signup');
        await page.fill('input[name="firstName"]', 'Test');
        await page.fill('input[name="lastName"]', 'Seeker');
        await page.fill('input[name="email"]', 'newseeker@example.com');
        await page.fill('input[name="password"]', 'NewSeekerPass123!');
        await page.fill('input[name="repeatPassword"]', 'NewSeekerPass123!');
        await page.selectOption('select[name="role"]', 'seeker');
        await page.click('button[type="submit"]');
        // Fill seeker info form
        await expect(page).toHaveURL(baseURL + '/seekerinfo');
        await page.fill('input[name="phone"]', '0987654321');
        await page.fill('input[name="address"]', '456 Seeker Ave');
        await page.fill('input[name="city"]', 'SeekerCity');
        await page.fill('input[name="country"]', 'SeekerCountry');
        await page.selectOption('select[name="gender"]', 'Other');
        // Upload a dummy document file
        const filePath = require('path').resolve(__dirname, 'dummy_document.txt');
        await page.setInputFiles('input[name="document"]', filePath);
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(baseURL + '/seekerdashboard');
        await expect(page.locator('text=Seeker Dashboard')).toBeVisible();
    });

    test('Navigate and interact with all main pages and buttons', async({ page }) => {
        // Pages to test
        const pages = [
            { url: '/', text: 'Home' },
            { url: '/about', text: 'About' },
            { url: '/searchjob', text: 'Search Jobs', login: true, role: 'seeker' },
            { url: '/setting', text: 'Settings', login: true, role: 'seeker' },
            { url: '/profile', text: 'Profile', login: true, role: 'seeker' },
            { url: '/postjobs', text: 'Post Jobs', login: true, role: 'publisher' },
            { url: '/publisherdashboard', text: 'Publisher Dashboard', login: true, role: 'publisher' },
            { url: '/seekerdashboard', text: 'Seeker Dashboard', login: true, role: 'seeker' },
            { url: '/publisherprofile', text: 'Publisher Profile', login: true, role: 'publisher' },
            { url: '/editpublisherprofile', text: 'Edit Publisher Profile', login: true, role: 'publisher' },
            { url: '/editprofile', text: 'Edit Profile', login: true, role: 'seeker' },
            { url: '/postjobs', text: 'Post Jobs', login: true, role: 'publisher' }
        ];

        // Helper function to login
        async function loginAs(page, role) {
            await page.goto(baseURL + '/login');
            if (role === 'seeker') {
                await page.fill('input[name="email"]', 'seeker@example.com');
                await page.fill('input[name="password"]', 'SeekerPass123!');
            } else if (role === 'publisher') {
                await page.fill('input[name="email"]', 'publisher@example.com');
                await page.fill('input[name="password"]', 'PublisherPass123!');
            }
            await page.click('button[type="submit"]');
        }

        for (const p of pages) {
            if (p.login) {
                await loginAs(page, p.role);
            }
            await page.goto(baseURL + p.url);
            await expect(page.locator(`text=${p.text}`)).toBeVisible();

            // Interact with buttons and links on the page
            const buttons = await page.$$('button, a');
            for (const button of buttons) {
                try {
                    await button.click();
                    // Wait a bit for navigation or UI update
                    await page.waitForTimeout(500);
                    // Go back if navigation happened
                    if (page.url() !== baseURL + p.url) {
                        await page.goBack();
                    }
                } catch (e) {
                    // Ignore errors from disabled buttons or navigation issues
                }
            }

            // Logout after publisher or seeker pages
            if (p.login) {
                await page.goto(baseURL + '/logout');
            }
        }
    });

});