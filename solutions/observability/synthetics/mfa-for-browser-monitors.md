---
navigation_title: Multi-factor Authentication
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-mfa.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-mfa.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Multi-factor Authentication (MFA) for browser monitors [synthetics-mfa]

Multi-factor Authentication (MFA) adds an essential layer of security to applications login processes, protecting against unauthorized access. A very common use case in Synthetics is testing user journeys involving websites protected by MFA.

Synthetics supports testing websites secured by Time-based One-Time Password (TOTP), a common MFA method that provides short-lived one-time tokens to enhance security.

## Configuring TOTP for MFA [configuring_totp_for_mfa]

To test a browser journey that uses TOTP for MFA, first configure the Synthetics authenticator token in the target application. To do this, generate a One-Time Password (OTP) using the Synthetics CLI; refer to [`@elastic/synthetics totp <secret>`](/solutions/observability/synthetics/cli.md).

```sh
npx @elastic/synthetics totp <secret>

// prints
OTP Token: 123456
```

## Applying the TOTP Token in Browser Journeys [applying_the_totp_token_in_browser_journeys]

Once the Synthetics TOTP Authentication is configured in your application, you can now use the OTP token in the synthetics browser journeys using the `mfa` object imported from `@elastic/synthetics`.

```ts
import { journey, step, mfa} from '@elastic/synthetics';

journey('MFA Test', ({ page, params }) => {
  step('Login using TOTP token', async () => {
    // login using username and pass and go to 2FA in next page
    const token = mfa.totp(params.MFA_SECRET);
    await page.getByPlaceholder("token-input").fill(token)
  });
});
```

For monitors created in the Synthetics UI using the Script editor, the `mfa` object can be accessed as shown below:

```ts
step('Login using 2FA', async () => {
  const token = mfa.totp(params.MFA_SECRET);
  await page.getByPlaceholder("token-input").fill(token)
});
```

::::{note}
`params.MFA_SECRET` would be the encoded secret that was used for registering the Synthetics Authentication in your web application.

::::