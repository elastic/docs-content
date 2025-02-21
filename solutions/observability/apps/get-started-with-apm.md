---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-getting-started-apm-server.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-get-started.html

navigation_title: "Get started"
---

# Get started with APM [apm-getting-started-apm-server]


::::{note}
Starting in version 8.15.0, the {{es}} apm-data plugin manages APM index templates, lifecycle policies, and ingest pipelines.
::::


The APM Server receives performance data from your APM agents, validates and processes it, and then transforms the data into {{es}} documents. If you’re on this page, then you’ve chosen to self-manage the Elastic Stack, and you now must decide how to run and configure the APM Server. There are two options, and the components required are different for each:

* **[Fleet-managed APM Server](../../../solutions/observability/apps/get-started-with-apm.md#apm-setup-fleet-managed-apm)**
* **[APM Server binary](../../../solutions/observability/apps/get-started-with-apm.md#apm-setup-apm-server-binary)**


## Fleet-managed APM Server [apm-setup-fleet-managed-apm]

Fleet is a web-based UI in {{kib}} that is used to centrally manage {{agent}}s. In this deployment model, use {{agent}} to spin up APM Server instances that can be centrally-managed in a custom-curated user interface.

:::{image} ../../../images/observability-fm-ov.png
:alt: APM Server fleet overview
:::

**Pros**:

* Conveniently manage one, some, or many different integrations from one central {{fleet}} UI.
* Centrally manage multiple APM Servers running on edge machines.

**Supported outputs**:

* {{es}}
* {{ess}}

::::{note}
Fleet-managed APM Server does *not* support all the outputs that are supported by the APM Server binary method of running Elastic APM.
::::


**Required components**:

* APM agents
* {{agent}} (which runs multiple subprocesses including APM Server, Fleet Server, and {{stack}})

**Configuration method**: {{kib}} UI


## APM Server binary [apm-setup-apm-server-binary]

Install, configure, and run the APM Server binary wherever you need it.

:::{image} ../../../images/observability-bin-ov.png
:alt: APM Server binary overview
:::

**Pros**:

* Simplest self-managed option
* No addition component knowledge required
* YAML configuration simplifies automation

**Supported outputs**:

* {{es}}
* {{ess}}
* {{ls}}
* Kafka
* Redis
* File
* Console

**Required components**:

* APM agents
* APM Server
* {{stack}}

**Configuration method**: YAML


## Help me decide [_help_me_decide]

This decision tree highlights key factors to help you make an informed decision about implementing Elastic APM. It provides practical guidance and is not intended to serve as a comprehensive reference of all possible implementations and capabilities.

<div style="width:100%;margin-bottom:30px" >
<!-- This SVG was created in Figma. Find the source in the obs-docs team space. -->
<svg viewBox="0 0 844 798" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="437" y="679" width="313" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="511.155" y="744.545">APM Server binary</tspan></text>
<rect x="67" y="679" width="313" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="102.167" y="744.545">Fleet-managed APM Server</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="418.334" y="582.591">YAML</tspan></text>
<path d="M413.5 578L386 578" stroke="#017D73" stroke-width="2"/>
<path d="M492.707 671.707C492.317 672.098 491.683 672.098 491.293 671.707L484.929 665.343C484.538 664.953 484.538 664.319 484.929 663.929C485.319 663.538 485.953 663.538 486.343 663.929L492 669.586L497.657 663.929C498.047 663.538 498.681 663.538 499.071 663.929C499.462 664.319 499.462 664.953 499.071 665.343L492.707 671.707ZM491 671L491 590L493 590L493 671L491 671ZM480 579L465 579L465 577L480 577L480 579ZM491 590C491 583.925 486.075 579 480 579L480 577C487.18 577 493 582.82 493 590L491 590Z" fill="#017D73"/>
<path d="M1 738L0.999998 598C0.999998 591.373 6.37258 586 13 586L23 586" stroke="#017D73" stroke-width="2"/>
<path d="M63 586L45.5 586" stroke="#017D73" stroke-width="2"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="27.4316" y="591.591">UI</tspan></text>
<rect x="67" y="521" width="313" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="130.668" y="610.568">Curated UI or YAML-based?</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="87.9408" y="563.568">What is your preferred method </tspan><tspan x="147.258" y="585.568">of configuration?
</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="214.353" y="491.591">no</tspan></text>
<line x1="223" y1="468" x2="223" y2="478" stroke="#017D73" stroke-width="2"/>
<path d="M222.293 512.707C222.683 513.098 223.317 513.098 223.707 512.707L230.071 506.343C230.462 505.953 230.462 505.319 230.071 504.929C229.681 504.538 229.047 504.538 228.657 504.929L223 510.586L217.343 504.929C216.953 504.538 216.319 504.538 215.929 504.929C215.538 505.319 215.538 505.953 215.929 506.343L222.293 512.707ZM222 496L222 512L224 512L224 496L222 496Z" fill="#017D73"/>
<path d="M1 738L0.999995 415C0.999995 408.373 6.37258 403 13 403L19 403" stroke="#017D73" stroke-width="2"/>
<path d="M63 403L51 403" stroke="#017D73" stroke-width="2"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="23.4072" y="406.591">yes</tspan></text>
<rect x="67" y="345" width="313" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="81.0395" y="426.068">Integrations collect observability data from </tspan><tspan x="90.5346" y="443.068">specific services and protect endpoints.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="113.359" y="379.068">Do you want to use other </tspan><tspan x="88.6703" y="401.068">integrations with APM Server?
</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="646.018" y="525.591">Logstash or
</tspan><tspan x="666.778" y="542.591">Kafka</tspan></text>
<path d="M686 471L686 511" stroke="#017D73" stroke-width="2"/>
<path d="M686.707 672.707C686.317 673.098 685.683 673.098 685.293 672.707L678.929 666.343C678.538 665.953 678.538 665.319 678.929 664.929C679.319 664.538 679.953 664.538 680.343 664.929L686 670.586L691.657 664.929C692.047 664.538 692.681 664.538 693.071 664.929C693.462 665.319 693.462 665.953 693.071 666.343L686.707 672.707ZM687 549L687 672L685 672L685 549L687 549Z" fill="#017D73"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="413.741" y="410.591">Elasticsearch</tspan></text>
<path d="M527 406L510 406" stroke="#017D73" stroke-width="2"/>
<path d="M385.293 406.707C384.902 406.317 384.902 405.683 385.293 405.293L391.657 398.929C392.047 398.538 392.681 398.538 393.071 398.929C393.462 399.319 393.462 399.953 393.071 400.343L387.414 406L393.071 411.657C393.462 412.047 393.462 412.681 393.071 413.071C392.681 413.462 392.047 413.462 391.657 413.071L385.293 406.707ZM393.109 406L393.109 405L393.109 406ZM386 405L393.109 405L393.109 407L386 407L386 405ZM393.109 405L410 405L410 407L393.109 407L393.109 405Z" fill="#017D73"/>
<rect x="530" y="345" width="313" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="584.912" y="423.568">Most users need Elasticsearch</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="560.064" y="398.568">Which output are you using?
</tspan></text>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="12" letter-spacing="0em"><tspan x="546.669" y="256.545">APM agents live on </tspan><tspan x="541.625" y="271.545">edge machines </tspan><tspan x="650" y="271.545"> a </tspan><tspan x="542.82" y="286.545">single APM Server is </tspan><tspan x="555.236" y="301.545">hosted centrally</tspan></text>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="12" font-style="italic" letter-spacing="0em"><tspan x="631.214" y="271.545">but</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="543.655" y="239.591">Centrally hosted</tspan></text>
<path d="M522 235H538" stroke="#017D73" stroke-width="2"/>
<path d="M686.707 337.707C686.317 338.098 685.683 338.098 685.293 337.707L678.929 331.343C678.538 330.953 678.538 330.319 678.929 329.929C679.319 329.538 679.953 329.538 680.343 329.929L686 335.586L691.657 329.929C692.047 329.538 692.681 329.538 693.071 329.929C693.462 330.319 693.462 330.953 693.071 331.343L686.707 337.707ZM685 337L685 246.841L687 246.841L687 337L685 337ZM674 235.841L660.5 235.841L660.5 233.841L674 233.841L674 235.841ZM685 246.841C685 240.766 680.075 235.841 674 235.841L674 233.841C681.18 233.841 687 239.661 687 246.841L685 246.841Z" fill="#017D73"/>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="12" letter-spacing="0em"><tspan x="61.5117" y="256.749">APM agents </tspan><tspan x="154.488" y="256.749"> </tspan><tspan x="54.4863" y="271.749">APM Server live on </tspan><tspan x="52.5703" y="286.749">each edge machine</tspan></text>
<text fill="black" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="12" font-style="italic" letter-spacing="0em"><tspan x="133.254" y="256.749">and</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="55.9617" y="239.591">Edge machines</tspan></text>
<path d="M1 738L1.00015 247.443C1.00015 240.815 6.37273 235.443 13.0001 235.443L45.5 235.443M201 235.443L172.5 235.443" stroke="#017D73" stroke-width="2"/>
<rect x="206" y="176" width="311" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="237.179" y="254.568">Note that central is required for RUM.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="220.012" y="229.568">Where will you run APM Server?
</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="352.353" y="147.591">no</tspan></text>
<line x1="361" y1="125" x2="361" y2="135" stroke="#017D73" stroke-width="2"/>
<path d="M360.293 169.707C360.683 170.098 361.317 170.098 361.707 169.707L368.071 163.343C368.462 162.953 368.462 162.319 368.071 161.929C367.681 161.538 367.047 161.538 366.657 161.929L361 167.586L355.343 161.929C354.953 161.538 354.319 161.538 353.929 161.929C353.538 162.319 353.538 162.953 353.929 163.343L360.293 169.707ZM360 153L360 169L362 169L362 153L360 153Z" fill="#017D73"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="137.407" y="64.5909">yes</tspan></text>
<path d="M201 61.1904L171 61.1904" stroke="#017D73" stroke-width="2"/>
<path d="M51.7071 750.707C52.0976 750.317 52.0976 749.683 51.7071 749.293L45.3431 742.929C44.9526 742.538 44.3195 742.538 43.9289 742.929C43.5384 743.319 43.5384 743.953 43.9289 744.343L49.5858 750L43.9289 755.657C43.5384 756.047 43.5384 756.681 43.9289 757.071C44.3195 757.462 44.9526 757.462 45.3431 757.071L51.7071 750.707ZM13 61.8925L127 61.8925L127 59.8925L13 59.8925L13 61.8925ZM51 749L13 749L13 751L51 751L51 749ZM2.00001 738L2.00001 72.8925L6.90879e-06 72.8925L6.91526e-06 738L2.00001 738ZM13 749C6.92487 749 2.00001 744.075 2.00001 738L6.91526e-06 738C6.90287e-06 745.18 5.8203 751 13 751L13 749ZM13 59.8925C5.8203 59.8925 6.92117e-06 65.7128 6.90879e-06 72.8925L2.00001 72.8925C2.00001 66.8173 6.92488 61.8925 13 61.8925L13 59.8925Z" fill="#017D73"/>
<rect x="206" y="1" width="311" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="272.947" y="62.5682">Elastic Cloud simplifies the </tspan><tspan x="254.224" y="79.5682">management and deployment of </tspan><tspan x="320.642" y="96.5682">Elastic APM.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="236.379" y="37.5682">Are you using Elastic Cloud?
</tspan></text>
</svg>
</div>


% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/docs-content/serverless/observability-apm-get-started.md