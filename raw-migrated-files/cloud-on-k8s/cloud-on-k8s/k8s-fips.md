# Deploy a FIPS compatible version of ECK [k8s-fips]

The Federal Information Processing Standard (FIPS) Publication 140-2, (FIPS PUB 140-2), titled "Security Requirements for Cryptographic Modules" is a U.S. government computer security standard used to approve cryptographic modules. Since version 2.6 ECK offers a FIPS-enabled image that is a drop-in replacement for the standard image.

For the ECK operator, adherence to FIPS 140-2 is ensured by:

* Using FIPS approved / NIST recommended cryptographic algorithms.
* Compiling the operator using the [BoringCrypto](https://github.com/golang/go/blob/dev.boringcrypto/README.boringcrypto.md) library for various cryptographic primitives.


