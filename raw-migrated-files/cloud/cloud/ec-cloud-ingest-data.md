# Adding data to Elasticsearch [ec-cloud-ingest-data]

You have a number of options for getting data into Elasticsearch, referred to as ingesting or indexing your data. Use Elastic Agent, Beats, Logstash, Elastic language clients, Elastic connectors, or the Enterprise Search web crawler. The option (or combination) selected depends on whether you are indexing general content or timestamped data.

$$$ec-ingest-methods$$$

General content
:   Index content like HTML pages, catalogs and other files. Send data directly to Elasticseach from your application using an Elastic language client. Otherwise use Elastic content [connectors](https://www.elastic.co/guide/en/enterprise-search/current/connectors.html) or the Elastic [web crawler](https://www.elastic.co/guide/en/enterprise-search/current/crawler.html).

Timestamped data
:   The preferred way to index timestamped data is to use Elastic Agent. Elastic Agent is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, and forward data from remote services or hardware. Each Elastic Agent based integration includes default ingestion rules, dashboards, and visualizations to start analyzing your data right away. Fleet Management enables you to centrally manage all of your deployed Elastic Agents from Kibana.

    If no Elastic Agent integration is available for your data source, use Beats to collect your data. Beats are data shippers designed to collect and ship a particular type of data from a server. You install a separate Beat for each type of data to collect. Modules that provide default configurations, Elasticsearch ingest pipeline definitions, and Kibana dashboards are available for some Beats, such as Filebeat and Metricbeat. No Fleet management capabilities are provided for Beats.

    If neither Elastic Agent or Beats supports your data source, use Logstash. Logstash is an open source data collection engine with real-time pipelining capabilities that supports a wide variety of data sources. You might also use Logstash to persist incoming data to ensure data is not lost if there’s an ingestion spike, or if you need to send the data to multiple destinations.



## Designing a data ingestion pipeline [ec-data-ingest-pipeline]

While you can send data directly to Elasticsearch, data ingestion pipelines often include additional steps to manipulate the data, ensure data integrity, or manage the data flow.

::::{note}
This diagram focuses on *timestamped* data.

::::


<div style="width:100%;margin-bottom:30px" >
<!-- This SVG was created in Figma. Find the source in the obs-docs team space. -->
<svg viewBox="0 0 1057 1212" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="428" y="1093" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="454.583" y="1147.55">Start sending data to </tspan><tspan x="487.524" y="1169.55">Elasticsearch</tspan></text>
<path d="M509.293 1084.71C509.683 1085.1 510.317 1085.1 510.707 1084.71L517.071 1078.34C517.462 1077.95 517.462 1077.32 517.071 1076.93C516.681 1076.54 516.047 1076.54 515.657 1076.93L510 1082.59L504.343 1076.93C503.953 1076.54 503.319 1076.54 502.929 1076.93C502.538 1077.32 502.538 1077.95 502.929 1078.34L509.293 1084.71ZM157 1000V1039.48H159V1000H157ZM170 1052.48H498V1050.48H170V1052.48ZM509 1063.48V1084H511V1063.48H509ZM498 1052.48C504.075 1052.48 509 1057.41 509 1063.48H511C511 1056.3 505.18 1050.48 498 1050.48V1052.48ZM157 1039.48C157 1046.66 162.82 1052.48 170 1052.48V1050.48C163.925 1050.48 159 1045.56 159 1039.48H157Z" fill="#017D73"/>
<path d="M530.293 1084.71C530.683 1085.1 531.317 1085.1 531.707 1084.71L538.071 1078.34C538.462 1077.95 538.462 1077.32 538.071 1076.93C537.681 1076.54 537.047 1076.54 536.657 1076.93L531 1082.59L525.343 1076.93C524.953 1076.54 524.319 1076.54 523.929 1076.93C523.538 1077.32 523.538 1077.95 523.929 1078.34L530.293 1084.71ZM401 1000V1015.77H403V1000H401ZM414 1028.77H519V1026.77H414V1028.77ZM530 1039.77V1084H532V1039.77H530ZM519 1028.77C525.075 1028.77 530 1033.7 530 1039.77H532C532 1032.59 526.18 1026.77 519 1026.77V1028.77ZM401 1015.77C401 1022.95 406.82 1028.77 414 1028.77V1026.77C407.925 1026.77 403 1021.85 403 1015.77H401Z" fill="#017D73"/>
<path d="M573.707 1084.71C573.317 1085.1 572.683 1085.1 572.293 1084.71L565.929 1078.34C565.538 1077.95 565.538 1077.32 565.929 1076.93C566.319 1076.54 566.953 1076.54 567.343 1076.93L573 1082.59L578.657 1076.93C579.047 1076.54 579.681 1076.54 580.071 1076.93C580.462 1077.32 580.462 1077.95 580.071 1078.34L573.707 1084.71ZM926 1000V1039.48H924V1000H926ZM913 1052.48H585V1050.48H913V1052.48ZM574 1063.48V1084H572V1063.48H574ZM585 1052.48C578.925 1052.48 574 1057.41 574 1063.48H572C572 1056.3 577.82 1050.48 585 1050.48V1052.48ZM926 1039.48C926 1046.66 920.18 1052.48 913 1052.48V1050.48C919.075 1050.48 924 1045.56 924 1039.48H926Z" fill="#017D73"/>
<path d="M552.707 1084.71C552.317 1085.1 551.683 1085.1 551.293 1084.71L544.929 1078.34C544.538 1077.95 544.538 1077.32 544.929 1076.93C545.319 1076.54 545.953 1076.54 546.343 1076.93L552 1082.59L557.657 1076.93C558.047 1076.54 558.681 1076.54 559.071 1076.93C559.462 1077.32 559.462 1077.95 559.071 1078.34L552.707 1084.71ZM682 1000V1015.77H680V1000H682ZM669 1028.77H564V1026.77H669V1028.77ZM553 1039.77V1084H551V1039.77H553ZM564 1028.77C557.925 1028.77 553 1033.7 553 1039.77H551C551 1032.59 556.82 1026.77 564 1026.77V1028.77ZM682 1015.77C682 1022.95 676.18 1028.77 669 1028.77V1026.77C675.075 1026.77 680 1021.85 680 1015.77H682Z" fill="#017D73"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="315.853" y="682.591">no</tspan></text>
<path d="M412.207 1150.71C412.598 1150.32 412.598 1149.68 412.207 1149.29L405.843 1142.93C405.453 1142.54 404.82 1142.54 404.429 1142.93C404.039 1143.32 404.039 1143.95 404.429 1144.34L410.086 1150L404.429 1155.66C404.039 1156.05 404.039 1156.68 404.429 1157.07C404.82 1157.46 405.453 1157.46 405.843 1157.07L412.207 1150.71ZM310 677.601L13.5002 677.601L13.5002 679.601L310 679.601L310 677.601ZM0.500274 690.601L0.500258 1138L2.50026 1138L2.50027 690.601L0.500274 690.601ZM13.5003 1151L411.5 1151L411.5 1149L13.5003 1149L13.5003 1151ZM0.500258 1138C0.500257 1145.18 6.32057 1151 13.5003 1151L13.5003 1149C7.42512 1149 2.50026 1144.08 2.50026 1138L0.500258 1138ZM13.5002 677.601C6.32056 677.601 0.500274 683.421 0.500274 690.601L2.50027 690.601C2.50027 684.525 7.42514 679.601 13.5002 679.601L13.5002 677.601Z" fill="#BD271E"/>
<path d="M339 678.158L414 678.158" stroke="#BD271E" stroke-width="2"/>
<rect x="818" y="877" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="857.135" y="938.568">Process data using </tspan><tspan x="896.422" y="955.568"> and forward it with </tspan><tspan x="982.377" y="972.568">.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="842.526" y="913.568">Use Logstash plugins
</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="986.813" y="938.568"><a href="{{logstash-ref}}/filter-plugins.html">filter </a></tspan><tspan x="849.076" y="955.568"><a href="{{logstash-ref}}/filter-plugins.html">plugins</a></tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="887.767" y="972.568"><a href="{{logstash-ref}}/output-plugins.html">output plugins</a></tspan></text>
<rect x="558" y="877" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="577.482" y="947.068">Use </tspan><tspan x="697.302" y="947.068"> with Elastic </tspan><tspan x="625.942" y="964.068">Agent or Beats.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="596.887" y="922.068">Use runtime fields
</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="607.259" y="947.068"><a href="{{ref}}/runtime.html">runtime fields</a></tspan></text>
<rect x="298" y="877" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="335.796" y="947.068">Use a pipeline for </tspan><tspan x="405.358" y="964.068"> or </tspan><tspan x="464.202" y="964.068">.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="328.002" y="922.068">Use ingest pipelines
</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="455.083" y="947.068"><a href="{{ref}}/ingest.html#pipelines-for-fleet-elastic-agent">Elastic </a></tspan><tspan x="365.942" y="964.068"><a href="{{ref}}/ingest.html#pipelines-for-fleet-elastic-agent">Agent</a></tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="426.796" y="964.068"><a href="{{ref}}/ingest.html#pipelines-for-beats">Beats</a></tspan></text>
<rect x="37.9995" y="877" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="57.9741" y="938.568">For Elastic Agent integrations, </tspan><tspan x="64.0308" y="955.568">use an </tspan><tspan x="220.957" y="955.568">. For </tspan><tspan x="59.0747" y="972.568">Beats, use a </tspan><tspan x="251.069" y="972.568">.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="88.2251" y="913.568">Use processors
</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="143.704" y="972.568"><a href="{{filebeat-ref}}/filtering-and-enhancing-data.html">Beats processor</a></tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="111.582" y="955.568"><a href="{{fleet-guide}}/elastic-agent-processor-configuration.html">Agent processor</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="811.555" y="820.591">something
</tspan><tspan x="834.004" y="837.591">else</tspan></text>
<path d="M573 722V731.5C573 738.127 578.372 743.5 585 743.5L836.139 743.5C842.766 743.5 848.139 748.873 848.139 755.5L848.139 805" stroke="#017D73" stroke-width="2"/>
<path d="M848.736 871.707C848.345 872.098 847.712 872.098 847.322 871.707L840.958 865.343C840.567 864.953 840.567 864.319 840.958 863.929C841.348 863.538 841.981 863.538 842.372 863.929L848.029 869.586L853.685 863.929C854.076 863.538 854.709 863.538 855.1 863.929C855.49 864.319 855.49 864.953 855.1 865.343L848.736 871.707ZM847.029 871L847.029 845.023L849.029 845.023L849.029 871L847.029 871Z" fill="#017D73"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="615.153" y="818.591">define or alter the </tspan><tspan x="602.076" y="835.591">schema at query time</tspan></text>
<path d="M674.293 872.708C674.683 873.099 675.317 873.099 675.707 872.708L682.071 866.344C682.462 865.954 682.462 865.321 682.071 864.93C681.681 864.54 681.047 864.54 680.657 864.93L675 870.587L669.343 864.93C668.953 864.54 668.319 864.54 667.929 864.93C667.538 865.321 667.538 865.954 667.929 866.344L674.293 872.708ZM674 843L674 872.001L676 872.001L676 843L674 843Z" fill="#017D73"/>
<path d="M552 722L552 752C552 758.627 557.372 764 564 764L663 764C669.627 764 675 769.373 675 776L675 805" stroke="#017D73" stroke-width="2"/>
<path d="M413.639 871.707C414.03 872.098 414.663 872.098 415.053 871.707L421.417 865.343C421.808 864.953 421.808 864.319 421.417 863.929C421.027 863.538 420.394 863.538 420.003 863.929L414.346 869.586L408.689 863.929C408.299 863.538 407.666 863.538 407.275 863.929C406.885 864.319 406.885 864.953 407.275 865.343L413.639 871.707ZM413.346 851.5L413.346 871L415.346 871L415.346 851.5L413.346 851.5Z" fill="#017D73"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="342.301" y="809.591">convert data to ECS, </tspan><tspan x="333.817" y="826.591">normalize field data, or </tspan><tspan x="339.942" y="843.591">enrich incoming data</tspan></text>
<path d="M531 722L531 752C531 758.627 525.627 764 519 764L426 764C419.372 764 414 769.373 414 776L414 793.5" stroke="#017D73" stroke-width="2"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="75.2744" y="818.591">sanitize or enrich raw </tspan><tspan x="86.9571" y="835.591">data at the source</tspan></text>
<path d="M510 722L510 732C510 738.627 504.627 744 498 744L161 744C154.372 744 149 749.373 149 756L149 801.5" stroke="#017D73" stroke-width="2"/>
<path d="M148.638 871.707C149.029 872.098 149.662 872.098 150.053 871.707L156.417 865.343C156.807 864.953 156.807 864.319 156.417 863.929C156.026 863.538 155.393 863.538 155.002 863.929L149.346 869.586L143.689 863.929C143.298 863.538 142.665 863.538 142.275 863.929C141.884 864.319 141.884 864.953 142.275 865.343L148.638 871.707ZM150.346 871L150.346 845.5L148.346 845.5L148.346 871L150.346 871Z" fill="#017D73"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="904.121" y="767.591">to enrich </tspan><tspan x="919.208" y="784.591">data</tspan></text>
<line x1="934" y1="722" x2="934" y2="754" stroke="#017D73" stroke-width="2"/>
<path d="M933.293 871.707C933.683 872.098 934.316 872.098 934.707 871.707L941.071 865.343C941.461 864.953 941.461 864.319 941.071 863.929C940.68 863.538 940.047 863.538 939.657 863.929L934 869.586L928.343 863.929C927.952 863.538 927.319 863.538 926.929 863.929C926.538 864.319 926.538 864.953 926.929 865.343L933.293 871.707ZM933 793L933 871L935 871L935 793L933 793Z" fill="#017D73"/>
<rect x="818" y="595" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="908.639" y="666.068"> using one (or more) </tspan><tspan x="977.846" y="683.068">.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="877.655" y="641.068">Use Logstash
</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="833.238" y="666.068"><a href="{{logstash-ref}}/getting-started-with-logstash.html">Get started</a></tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="893.299" y="683.068"><a href="{{logstash-ref}}/input-plugins.html">input plugins</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="844.086" y="352.591">no</tspan></text>
<path d="M773 325L773 337C773 343.627 778.372 349 785 349L838 349" stroke="#BD271E" stroke-width="2"/>
<path d="M934.707 587.707C934.316 588.098 933.683 588.098 933.293 587.707L926.929 581.343C926.538 580.953 926.538 580.319 926.929 579.929C927.319 579.538 927.952 579.538 928.343 579.929L934 585.586L939.657 579.929C940.047 579.538 940.68 579.538 941.071 579.929C941.461 580.319 941.461 580.953 941.071 581.343L934.707 587.707ZM933 587L933 361L935 361L935 587L933 587ZM922 350L869 350L869 348L922 348L922 350ZM933 361C933 354.925 928.075 350 922 350L922 348C929.18 348 935 353.82 935 361L933 361Z" fill="#BD271E"/>
<rect x="428" y="595" width="238" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="481.407" y="650.545">Do you need to </tspan><tspan x="462.757" y="672.545">process your data?</tspan></text>
<path d="M541.294 587.746C541.684 588.115 542.316 588.08 542.706 587.668L549.06 580.956C549.45 580.544 549.45 579.911 549.06 579.542C548.67 579.173 548.038 579.207 547.648 579.619L542 585.586L536.351 580.239C535.961 579.87 535.329 579.904 534.939 580.316C534.549 580.728 534.549 581.361 534.939 581.73L541.294 587.746ZM541.001 521.055L541.001 587.055L542.998 586.945L542.998 520.945L541.001 521.055Z" fill="#017D73"/>
<rect x="428" y="397" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="527.305" y="467.068"> with the </tspan><tspan x="642.094" y="467.068"> </tspan><tspan x="529.958" y="484.068">Beat.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="491.725" y="442.068">Set up Beats
</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="451.905" y="467.068"><a href="{{beats-ref}}/getting-started.html">Get started</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="589.007" y="467.068">relevant</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="602.407" y="361.639">yes</tspan></text>
<path d="M681.5 325L681.5 345.476C681.5 352.104 676.127 357.476 669.5 357.476L631 357.476" stroke="#017D73" stroke-width="2"/>
<path d="M546.293 391.707C546.683 392.098 547.316 392.098 547.707 391.707L554.071 385.343C554.461 384.953 554.461 384.319 554.071 383.929C553.68 383.538 553.047 383.538 552.656 383.929L547 389.586L541.343 383.929C540.952 383.538 540.319 383.538 539.929 383.929C539.538 384.319 539.538 384.953 539.929 385.343L546.293 391.707ZM547 370.524L546 370.524L547 370.524ZM548 391L548 370.524L546 370.524L546 391L548 391ZM559 359.524L597.5 359.524L597.5 357.524L559 357.524L559 359.524ZM548 370.524C548 364.449 552.925 359.524 559 359.524L559 357.524C551.82 357.524 546 363.344 546 370.524L548 370.524Z" fill="#017D73"/>
<rect x="608" y="199" width="238" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="621.09" y="280.068">Look for your data source in the </tspan><tspan x="624.248" y="297.068">list of </tspan><tspan x="701.973" y="297.068"> and their modules.</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="664.566" y="297.068"><a href="{{beats-ref}}/beats-reference.html">Beats</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="751.839" y="233.068">Beats </tspan><tspan x="647.39" y="255.068">module</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="651.081" y="233.068">Is a Beat or </tspan><tspan x="713.149" y="255.068"> available?
</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="650.852" y="162.591">no</tspan></text>
<path d="M593 127L593 146C593 152.627 598.372 158 605 158L643.5 158" stroke="#BD271E" stroke-width="2"/>
<path d="M728.207 190.707C727.816 191.098 727.183 191.098 726.793 190.707L720.429 184.343C720.038 183.953 720.038 183.319 720.429 182.929C720.819 182.538 721.452 182.538 721.843 182.929L727.5 188.586L733.156 182.929C733.547 182.538 734.18 182.538 734.571 182.929C734.961 183.319 734.961 183.953 734.571 184.343L728.207 190.707ZM726.5 190L726.5 171L728.5 171L728.5 190L726.5 190ZM715.5 160L677 160L677 158L715.5 158L715.5 160ZM726.5 171C726.5 164.925 721.575 160 715.5 160L715.5 158C722.679 158 728.5 163.82 728.5 171L726.5 171Z" fill="#BD271E"/>
<path d="M415.707 640.707C416.097 640.317 416.097 639.683 415.707 639.293L409.343 632.929C408.952 632.538 408.319 632.538 407.929 632.929C407.538 633.319 407.538 633.953 407.929 634.343L413.586 640L407.929 645.657C407.538 646.047 407.538 646.681 407.929 647.071C408.319 647.462 408.952 647.462 409.343 647.071L415.707 640.707ZM378 640L378 639L378 640ZM365 325L365 628L367 628L367 325L365 325ZM378 641L415 641L415 639L378 639L378 641ZM365 628C365 635.18 370.82 641 378 641L378 639C371.925 639 367 634.075 367 628L365 628Z" fill="#017D73"/>
<rect x="248" y="199" width="238" height="118" rx="7" fill="white" stroke="#D3DAE6" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="272.814" y="280.068">In Kibana’s main menu, go to </tspan><tspan x="357.963" y="297.068"> -> </tspan><tspan x="462.457" y="297.068">.</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="273.036" y="233.068">Install the integration </tspan><tspan x="260.758" y="255.068">and set up Elastic Agent
</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="267.687" y="297.068">Management</tspan><tspan x="379.195" y="297.068">Integrations</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" font-weight="bold" letter-spacing="0em"><tspan x="422.407" y="162.591">yes</tspan></text>
<path d="M501.5 127L501.5 146C501.5 152.627 496.127 158 489.5 158L451 158" stroke="#017D73" stroke-width="2"/>
<path d="M366.293 190.707C366.683 191.098 367.316 191.098 367.707 190.707L374.071 184.343C374.461 183.953 374.461 183.319 374.071 182.929C373.68 182.538 373.047 182.538 372.657 182.929L367 188.586L361.343 182.929C360.952 182.538 360.319 182.538 359.929 182.929C359.538 183.319 359.538 183.953 359.929 184.343L366.293 190.707ZM368 190L368 171L366 171L366 190L368 190ZM379 160L417.5 160L417.5 158L379 158L379 160ZM368 171C368 164.925 372.925 160 379 160L379 158C371.82 158 366 163.82 366 171L368 171Z" fill="#017D73"/>
<rect x="428" y="1" width="238" height="118" rx="7" fill="#D3DAE6" fill-opacity="0.5" stroke="#69707D" stroke-width="2" stroke-linejoin="round"/>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="478.442" y="82.0682"> the</tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em"><tspan x="449.936" y="82.0682">Visit</tspan><tspan x="504.05" y="82.0682"> </tspan><tspan x="615.352" y="82.0682"> and </tspan><tspan x="462.467" y="99.0682">look for your data source.</tspan></text>
<text fill="#006BB4" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="14" letter-spacing="0em" text-decoration="underline"><tspan x="507.987" y="82.0682"><a href="https://docs.elastic.co/integrations">integration docs</a></tspan></text>
<text fill="#343741" xml:space="preserve" style="white-space: pre" font-family="Inter" font-size="18" font-weight="bold" letter-spacing="0em"><tspan x="466.211" y="35.0682">Is an Elastic Agent </tspan><tspan x="452.368" y="57.0682">integration available?
</tspan></text>
</svg>
</div>

### Data manipulation [ec-data-manipulation]

It’s often necessary to sanitize, normalize, transform, or enrich your data before it’s indexed and stored in Elasticsearch.

* Elastic Agent and Beats processors enable you to manipulate the data at the edge. This is useful if you need to control what data is sent across the wire, or need to enrich the raw data with information available on the host.
* Elasticsearch ingest pipelines enable you to manipulate the data as it comes in. This avoids putting additional processing overhead on the hosts from which you’re collecting data.
* Logstash enables you to avoid heavyweight processing at the edge, but still manipulate the data before sending it to Elasticsearch. This also enables you to send the processed data to multiple destinations.

One reason for preprocessing your data is to control the structure of the data that’s indexed into Elasticsearch—​the data schema. For example, use an ingest pipeline to map your data to the Elastic Common Schema (ECS). Alternatively, use runtime fields at query time to:

* Start working with your data without needing to understand how it’s structured
* Add fields to existing documents without reindexing your data
* Override the value returned from an indexed field
* Define fields for a specific use without modifying the underlying schema


### Data integrity [ec-data-integrity]

Logstash boosts data resiliency for important data that you don’t want to lose. Logstash offers an on-disk [persistent queue (PQ)](https://www.elastic.co/guide/en/logstash/current/persistent-queues.html) that absorbs bursts of events without an external buffering mechanism. It attempts to deliver messages stored in the PQ until delivery succeeds at least once.

The Logstash [dead letter queue (DLQ)](https://www.elastic.co/guide/en/logstash/current/dead-letter-queues.html) provides on-disk storage for events that Logstash can’t process, giving you a chance to evaluate them. You can use the dead_letter_queue input plugin to easily reprocess DLQ events.


### Data flow [ec-data-flow]

If you need to collect data from multiple Beats or Elastic Agents, consider using Logstash as a proxy. Logstash can receive data from multiple endpoints, even on different networks, and send the data on to Elasticsearch through a single firewall rule. You get more security for less work than if you set up individual rules for each endpoint.

Logstash can send to multiple [outputs](https://www.elastic.co/guide/en/logstash/current/output-plugins.html) from a single pipeline to help you get the most value from your data.


## Where to go from here [ec-data-ingest-where-to-go]

We have guides and many hands-on tutorials to help get you started with ingesting data into your cluster.


### Ingest data for Elastic solutions [ec-ingest-solutions]

[Get started with Elastic Observability](https://www.elastic.co/guide/en/observability/current/observability-get-started.html)
:   Use Elastic Observability to gain deeper insight into the behavior of your applications and systems. Follow our guides to ingest various data types, such as [logs and metrics](https://www.elastic.co/guide/en/observability/current/logs-metrics-get-started.html), [traces and APM](https://www.elastic.co/guide/en/observability/current/traces-get-started.html), and [data from Splunk](https://www.elastic.co/guide/en/observability/current/splunk-get-started.html). There are also several [tutorials](https://www.elastic.co/guide/en/observability/current/observability-tutorials.html) to choose from.

[Add data to Elastic Security](https://www.elastic.co/guide/en/security/current/ingest-data.html)
:   Use Elastic Security to quickly detect, investigate, and respond to threats and vulnerabilities across your environment. You can use {{agent}} to ingest data into the [{{elastic-defend}} integration](https://www.elastic.co/guide/en/security/current/install-endpoint.html), or with many other [{{integrations}}](https://docs.elastic.co/en/integrations) that work together with {{elastic-sec}}. You can also [ingest data from Splunk](https://www.elastic.co/guide/en/observability/current/splunk-get-started.html) or from various third party collectors that ship [ECS compliant security data](https://www.elastic.co/guide/en/security/current/siem-field-reference.html).


### Ingest data with Elastic Agent, Beats, and Logstash [ec-ingest-timestamped]

For users who want to build their own solution, we can help you get started ingesting your data using Elasticsearch Platform products.

[Elastic integrations](https://www.elastic.co/integrations)
:   Elastic integrations are a streamlined way to connect your data to the {{stack}}. Integrations are available for popular services and platforms, like Nginx, AWS, and MongoDB, as well as many generic input types like log files.

[Beats and Elastic Agent comparison](../../../manage-data/ingest/tools.md)
:   {{beats}} and {{agent}} can both send data to {{es}} either directly or via {{ls}}. You can use this guide to determine which of these primary ingest tools best matches your use case.

[Introduction to Fleet management](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html)
:   {{fleet}} provides a web-based UI in Kibana for centrally managing Elastic Agents and their policies.

[{{ls}} introduction](https://www.elastic.co/guide/en/logstash/current/introduction.html)
:   Use {{ls}} to dynamically unify data from disparate sources and normalize the data into destinations of your choice.


### Ingest data with Elastic web crawler, connectors [ec-ingest-crawler-connectors]

[Add data with the web crawler](https://www.elastic.co/guide/en/enterprise-search/current/crawler.html)
:   Use the web crawler to programmatically discover, extract, and index searchable content from websites and knowledge bases.

[Add data with connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html)
:   Sync data from an original data source to an {{es}} index. Connectors enable you to create searchable, read-only replicas of your data sources.


### Ingest data from your application [ec-ingest-app]

[Elasticsearch language clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html)
:   Use the {{es}} language clients to ingest data from an application into {{es}}.

[Enterprise Search language clients](https://www.elastic.co/guide/en/enterprise-search/current/programming-language-clients.html)
:   The {{ents}} programming language client libraries provide native APIs for those languages to ingest data into {{ents}}, App Search, and Workplace Search.

[Application ingest tutorials](../../../manage-data/ingest/ingesting-data-from-applications.md)
:   These hands-on guides demonstrate how to use the {{es}} language clients to ingest data from your applications.


### Manipulate and pre-process your data [ec-ingest-manipulate]

[Ingest pipelines](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html)
:   {{es}} ingest pipelines let you perform common transformations on your data before indexing.

[{{agent}} processors](https://www.elastic.co/guide/en/fleet/current/elastic-agent-processor-configuration.html)
:   Use the {{agent}} lightweight processors to parse, filter, transform, and enrich data at the source.

[Creating a {{ls}} pipeline](https://www.elastic.co/guide/en/logstash/current/configuration.html)
:   Create a {{ls}} pipeline by stringing together plugins—​inputs, outputs, filters, and sometimes codecs—​in order to process your data during ingestion.


### Sample data [ec-ingest-sample-data]

If you’re just learning about Elastic and don’t have a particular use case in mind, you can [load one of the sample data sets](../../../manage-data/ingest/sample-data.md) in Kibana. Complete with sample visualizations, dashboards, and more, they provide a quick way to see what’s possible with Elastic.

