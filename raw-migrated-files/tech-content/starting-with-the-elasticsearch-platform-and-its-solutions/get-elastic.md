# Get Elastic [get-elastic]

{{ecloud}} enables you set up the {{stack}} and start using the Search, Observability, and Security solutions in minutes. You can deploy globally in any of the dozens of supported regions across Amazon Web Services (AWS), Google Cloud, and Microsoft Azure.

If you prefer to go the self-managed route, you can install the Elastic Stack on your own hardware or on a public, private, or hybrid cloud. If you are operating multiple clusters, consider using Elastic Cloud Enterprise or Elastic Cloud for Kubernetes to orchestrate your deployments.

<div style="width:100%;margin-bottom:30px" >
<!-- This SVG was created in Figma. Find the source in the obs-docs team space. -->
<svg viewBox="0 0 964 922" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="964" height="922" fill="#F5F5F5"/>
<rect x="1" y="464" width="962" height="457" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<rect x="363.127" y="783" width="238.749" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="407.091" y="826.545">Orchestrate your </tspan><tspan x="403.031" y="848.545">deployments with </tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="376.426" y="870.545"><a href="https://www.elastic.co/guide/en/cloud-enterprise/current/index.html">Elastic Cloud Enterprise</a></tspan></text>
<rect x="20.0593" y="783" width="238.749" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="36.6808" y="826.545"><a href="/deploy-manage/deploy/self-managed/deploy-cluster.md">Install the Elastic Stack </a></tspan><tspan x="46.0499" y="848.545"><a href="/deploy-manage/deploy/self-managed/deploy-cluster.md">distributions for your </a></tspan><tspan x="83.1486" y="870.545"><a href="/deploy-manage/deploy/self-managed/deploy-cluster.md">environment</a></tspan></text>
<rect x="704.188" y="560" width="238.749" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="716.899" y="603.545">Deploy the Elastic Stack </tspan><tspan x="744.039" y="625.545">with </tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="786.86" y="625.545"><a href="https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html">Elastic Cloud </a></tspan><tspan x="771.927" y="647.545"><a href="https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html">Kubernetes</a></tspan></text>
<rect x="363.127" y="563" width="238.749" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="398.399" y="595.545">Do you want to use </tspan><tspan x="419.818" y="617.545">Kubernetes to </tspan><tspan x="408.612" y="639.545">orchestrate your </tspan><tspan x="419.378" y="661.545">deployments?</tspan></text>
<rect x="20.0593" y="563" width="238.749" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="36.9365" y="617.545">Do you need to manage </tspan><tspan x="39.4941" y="639.545">multiple deployments?</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="20" font-weight="bold" letter-spacing="0em"><tspan x="100.793" y="516.273">Self-managed: Install and operate the Elastic Stack on your own infrastructure</tspan></text>
<path d="M138.727 782.707C139.117 783.098 139.751 783.098 140.141 782.707L146.505 776.343C146.896 775.953 146.896 775.319 146.505 774.929C146.114 774.538 145.481 774.538 145.091 774.929L139.434 780.586L133.777 774.929C133.387 774.538 132.753 774.538 132.363 774.929C131.972 775.319 131.972 775.953 132.363 776.343L138.727 782.707ZM138.434 682L138.434 782L140.434 782L140.434 682L138.434 682Z" fill="black"/>
<rect x="84.2622" y="719" width="110.343" height="26" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="130.786" y="735.591">no</tspan></text>
<path d="M481.794 782.707C482.185 783.098 482.818 783.098 483.209 782.707L489.573 776.343C489.963 775.953 489.963 775.319 489.573 774.929C489.182 774.538 488.549 774.538 488.158 774.929L482.502 780.586L476.845 774.929C476.454 774.538 475.821 774.538 475.431 774.929C475.04 775.319 475.04 775.953 475.431 776.343L481.794 782.707ZM481.502 682L481.502 782L483.502 782L483.502 682L481.502 682Z" fill="black"/>
<rect x="427.33" y="719" width="110.343" height="26" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="473.854" y="735.591">no</tspan></text>
<path d="M360.828 622.707C361.218 622.317 361.218 621.683 360.828 621.293L354.464 614.929C354.073 614.538 353.44 614.538 353.05 614.929C352.659 615.319 352.659 615.953 353.05 616.343L358.706 622L353.05 627.657C352.659 628.047 352.659 628.681 353.05 629.071C353.44 629.462 354.073 629.462 354.464 629.071L360.828 622.707ZM259.809 623H360.121V621H259.809V623Z" fill="#017D73"/>
<rect x="291.908" y="612" width="36.1124" height="20" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="297.872" y="625.591">yes</tspan></text>
<path d="M703.895 619.707C704.286 619.317 704.286 618.683 703.895 618.293L697.531 611.929C697.141 611.538 696.508 611.538 696.117 611.929C695.727 612.319 695.727 612.953 696.117 613.343L701.774 619L696.117 624.657C695.727 625.047 695.727 625.681 696.117 626.071C696.508 626.462 697.141 626.462 697.531 626.071L703.895 619.707ZM602.876 620H703.188V618H602.876V620Z" fill="#017D73"/>
<rect x="634.976" y="609" width="36.1124" height="20" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="640.939" y="622.591">yes</tspan></text>
<path d="M119.293 463.707C119.683 464.098 120.317 464.098 120.707 463.707L127.071 457.343C127.462 456.953 127.462 456.319 127.071 455.929C126.681 455.538 126.047 455.538 125.657 455.929L120 461.586L114.343 455.929C113.953 455.538 113.319 455.538 112.929 455.929C112.538 456.319 112.538 456.953 112.929 457.343L119.293 463.707ZM119 205L119 463L121 463L121 205L119 205Z" fill="black"/>
<rect x="66" y="320.584" width="110" height="26.832" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="112.353" y="337.271">no</tspan></text>
<rect x="340" y="1" width="623" height="443" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="20" font-weight="bold" letter-spacing="0em"><tspan x="438.893" y="54.2727">Elastic Cloud Hosted</tspan></text>
<rect x="360" y="306" width="236.125" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="378.91" y="338.545">Subscribe through the </tspan><tspan x="432.769" y="360.545">, </tspan><tspan x="480.652" y="360.545">, or </tspan><tspan x="564.833" y="360.545"> </tspan><tspan x="405.848" y="382.545">marketplace for  </tspan><tspan x="417.986" y="404.545">unified billing</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="390.3" y="360.545"><a href="https://aws.amazon.com/marketplace/pp/prodview-voru33wi6xs7k?trk=5fbc596b-6d2a-433a-8333-0bd1f28e84da&sc_channel=el&ultron=gobig&hulk=regpage&blade=elasticweb&gambit=mp-b">AWS</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="441.769" y="360.545"><a href="https://console.cloud.google.com/marketplace/product/elastic-prod/elastic-cloud?utm_source=elastic&utm_medium=regpage&utm_campaign=mp-b&pli=1">GCP</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="512.222" y="360.545"><a href="https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?ocid=elasticweb-regpage-gobig-b-hero">Azure</a></tspan></text>
<rect x="707" y="87" width="236" height="118" rx="7" fill="#00BFB3" fill-opacity="0.1" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="734.701" y="130.545">Sign up directly with </tspan><tspan x="725.753" y="152.545">Elastic and </tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em" text-decoration="underline"><tspan x="826.107" y="152.545"><a href="https://cloud.elastic.co/registration">get started </a></tspan><tspan x="792.568" y="174.545"><a href="https://cloud.elastic.co/registration">for free</a></tspan></text>
<rect x="360" y="87" width="236.125" height="118" rx="7" fill="#00BFB3" fill-opacity="0.1" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="377.819" y="130.545">Do you want to sign up </tspan><tspan x="397.56" y="152.545">through elastic.co </tspan><tspan x="373.46" y="174.545"> or your cloud provider?</tspan></text>
<path d="M706.973 146.707C707.363 146.317 707.363 145.683 706.973 145.293L700.609 138.929C700.218 138.538 699.585 138.538 699.195 138.929C698.804 139.319 698.804 139.953 699.195 140.343L704.851 146L699.195 151.657C698.804 152.047 698.804 152.681 699.195 153.071C699.585 153.462 700.218 153.462 700.609 153.071L706.973 146.707ZM597.125 147H706.266V145H597.125V147Z" fill="#017D73"/>
<rect x="613.992" y="136" width="75.4062" height="20" fill="white"/>
<g filter="url(#filter0_d_0_1)">
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="618.391" y="149.591">elastic.co</tspan></text>
</g>
<path d="M477.355 305.707C477.746 306.097 478.379 306.097 478.77 305.707L485.134 299.343C485.524 298.952 485.524 298.319 485.134 297.929C484.743 297.538 484.11 297.538 483.719 297.929L478.062 303.586L472.406 297.929C472.015 297.538 471.382 297.538 470.991 297.929C470.601 298.319 470.601 298.952 470.991 299.343L477.355 305.707ZM477.062 205L477.062 305L479.062 305L479.062 205L477.062 205Z" fill="black"/>
<rect x="423.492" y="242" width="109.141" height="26" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="428.536" y="258.591">cloud provider</tspan></text>
<path d="M340.707 146.707C341.098 146.317 341.098 145.683 340.707 145.293L334.343 138.929C333.953 138.538 333.319 138.538 332.929 138.929C332.538 139.319 332.538 139.953 332.929 140.343L338.586 146L332.929 151.657C332.538 152.047 332.538 152.681 332.929 153.071C333.319 153.462 333.953 153.462 334.343 153.071L340.707 146.707ZM240 147H340V145H240V147Z" fill="#017D73"/>
<rect x="272" y="136" width="36" height="20" fill="#D9D9D9"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="277.907" y="149.591">yes</tspan></text>
<rect x="1" y="87" width="238" height="118" rx="7" fill="#00BFB3" fill-opacity="0.2" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="23.46" y="131.545">Do you want Elastic to </tspan><tspan x="33.5762" y="153.545">install and manage   </tspan><tspan x="40.8711" y="175.545">your deployment?</tspan></text>
<defs>
<filter id="filter0_d_0_1" x="614.928" y="139.237" width="73.5405" height="18.9126" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
<feFlood flood-opacity="0" result="BackgroundImageFix"/>
<feColorMatrix in="SourceAlpha" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha"/>
<feOffset dy="4"/>
<feGaussianBlur stdDeviation="2"/>
<feComposite in2="hardAlpha" operator="out"/>
<feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0"/>
<feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_0_1"/>
<feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_0_1" result="shape"/>
</filter>
</defs>
</svg>
</div>

## Where to go from here [_where_to_go_from_here]

* [Overview of the {{stack}}](../../../get-started/the-stack.md)
* [Adding your data](/manage-data/ingest.md)
* [{{stack}} subscriptions](https://www.elastic.co/subscriptions)
* [Elastic pricing](https://www.elastic.co/pricing/)

