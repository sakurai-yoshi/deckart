"""One purpose classification, shared by the gallery and downloadable AI indexes.

The primary purpose is a browsing aid. Search still crosses all categories.
Namespace defaults are explicit authoring conventions, never keyword guesses.
"""

SPECS = (
    ('01-経営・意思決定','strategy','方針、選択肢、資源配分、事業の価値を伝える。','strategy decision priorities governance'),
    ('02-計画・進捗','planning','時期、段取り、依存関係、進み具合を伝える。','planning progress schedule milestones'),
    ('03-品質・改善','quality','検査、測定、原因、予防、改善の関係を伝える。','quality inspection measurement improvement'),
    ('04-生産・設備','production','作業、工程、設備、保全、能力の使い方を伝える。','production equipment maintenance operations'),
    ('05-調達・物流','supply-chain','購買、供給、在庫、保管、包装、配送を伝える。','procurement sourcing inventory logistics'),
    ('06-開発・技術','development','要求、構想、設計、試作、技術の検証を伝える。','development engineering design prototype'),
    ('07-安全・事業継続','safety','危険への備え、作業の安全、リスク、継続と復旧を伝える。','safety risk resilience continuity'),
    ('08-環境・資源','sustainability','資源、エネルギー、再使用、環境負荷を伝える。','environment sustainability energy resources'),
    ('09-組織・人材','people','役割、学習、協働、働き方、人材の成長を伝える。','people team learning organization'),
    ('10-顧客・営業','customer','顧客の要求、提案、販売、サービス、利用後の支援を伝える。','customer sales service support'),
    ('11-会計・収益','finance','費用、収益、資金、投資、会計の関係を伝える。','finance cost cash profit investment'),
    ('12-情報・データ','information','情報の管理、データの流れ、権限、システムを伝える。','data information security digital systems'),
    ('13-説明・伝達','communication','数値、根拠、条件、意味、注釈を読み取りやすくする。','communication annotation comparison evidence'),
    ('14-背景・装飾','backgrounds','光、質感、形で資料の印象と視線の流れを整える。','background texture light abstract'),
)
LABELS={i+1:spec[0] for i,spec in enumerate(SPECS)}
NAMESPACES={
    'decision':1,'strategy':1,'relation':1,'relationship':1,
    'plan':2,'planning':2,'quality':3,'manufacturing':4,'production':4,
    'supply':5,'development':6,'safety':7,'environment':8,'people':9,
    'customer':10,'finance':11,'technology':12,'operations':12,'data':12,
    'part':13,'chart':13,'background':14,
}

# Mixed-purpose namespaces are curated by their depicted action or relationship.
GROUPS={
1: '''
framework/swot framework/three-set-overlap framework/two-set-overlap
framework/decision-tree
illustration/agreement-documents illustration/thinking
part/control-and-context part/decision-reversibility part/necessary-and-sufficient
part/absolute-and-relative part/decision-review-trigger
part/delegated-decision-boundary
''',
2: '''
framework/annual-rhythm framework/company-timeline framework/phased-roadmap
process/phased-acceptance process/parallel-validation
illustration/planning illustration/project-planning illustration/change-adoption
part/action-commitment part/dependency-condition part/leading-and-lagging
part/delayed-effect
''',
3: '''
manufacturing/fault-isolation manufacturing/nonconforming-segregation
manufacturing/standard-exception-improvement process/quality-gates
process/double-loop-learning framework/pdca framework/learning-cycle
illustration/calibration-reference illustration/careful-inspection
illustration/issue-isolation illustration/material-testing illustration/precision-measurement
illustration/product-traceability illustration/sample-retention
illustration/first-article-check illustration/mistake-proof-connection
illustration/failure-investigation illustration/sample-label-verification
illustration/foreign-object-removal
part/temporary-and-permanent-action part/criterion-and-result
part/measurement-resolution part/local-and-whole-result
''',
4: '''
process/bottleneck-bypass
illustration/assembly-work illustration/cable-management illustration/component-sorting
illustration/equipment-maintenance illustration/instructions-and-product
illustration/machine-monitoring illustration/material-to-product
illustration/organized-tool-storage illustration/preventive-maintenance
illustration/production-coordination illustration/replaceable-module
illustration/spare-parts-readiness illustration/workplace-organization
illustration/clean-work-surface
''',
5: '''
illustration/moving-materials illustration/packing-products illustration/protective-packaging
illustration/receiving-materials illustration/shipment-consolidation
illustration/shipment-preparation illustration/stock-check
illustration/supplier-sample-comparison illustration/dual-source-readiness
illustration/purchase-negotiation illustration/demand-forecast-review
illustration/temperature-controlled-transport illustration/moisture-protected-storage
illustration/pallet-stability illustration/supplier-continuity
''',
6: '''
manufacturing/design-verification manufacturing/engineering-change-impact
illustration/idea-development illustration/prototype-development
illustration/prototype-realization illustration/shared-components
illustration/design-clearance illustration/controlled-experiment
''',
7: '''
planning/risk-response-matrix planning/scenario-triggered-response
operations/incident-containment operations/standby-failover
illustration/ergonomic-workstation illustration/safe-work-preparation
illustration/emergency-readiness illustration/lockout-readiness
illustration/slip-trip-prevention illustration/chemical-secondary-containment
illustration/safe-box-lifting
part/residual-risk
''',
8: '''
illustration/energy-saving illustration/material-reuse
illustration/reduced-packaging illustration/responsible-resource-use
illustration/returnable-packaging illustration/water-recirculation
illustration/heat-recovery illustration/repair-before-replacement
illustration/material-separation illustration/local-energy-storage
''',
9: '''
framework/onboarding framework/organization-tree
relation/shared-responsibility relationship/nested-responsibility
strategy/capability-stack strategy/cross-functional-handoffs
operations/responsibility-swimlane process/escalation
illustration/discussing illustration/learning illustration/learning-resources
illustration/listening illustration/sharing-information illustration/team-briefing
illustration/video-consultation illustration/newcomer-orientation
illustration/work-handover illustration/skill-practice illustration/inclusive-collaboration
illustration/focused-work illustration/rest-and-recovery illustration/workload-distribution
illustration/cross-functional-review illustration/team-recognition
part/execution-and-approval part/handover-and-acknowledgment
''',
10: '''
process/inquiry-triage planning/customer-journey-support
strategy/customer-value-roles framework/service-delivery
illustration/customer-feedback illustration/welcoming-visitor
illustration/product-demonstration illustration/after-sales-repair
illustration/customer-requirements-review illustration/service-appointment
''',
11: '''
illustration/budget-review illustration/cash-flow-planning illustration/investment-evaluation
illustration/invoice-reconciliation illustration/expense-receipt-check
part/sunk-and-future-cost part/fixed-and-variable-cost part/one-time-and-recurring-cost
''',
12: '''
relationship/controlled-system-layers relation/traceable-collection
illustration/access-permission illustration/connected-device-data
illustration/data-backup illustration/document-digitization illustration/document-review
illustration/document-routing illustration/file-sharing illustration/information-consolidation
illustration/organized-archive illustration/secure-disposal illustration/version-comparison
illustration/network-segmentation illustration/secure-authentication
illustration/data-quality-check illustration/revision-release
part/version-and-change
''',
13: '''
illustration/asking-question illustration/checking-documents illustration/explaining
illustration/reporting illustration/writing-notes process/approval-return
''',
}
ICON_GROUPS={
1: '''
icon/alignment icon/company icon/company-network icon/competitive-comparison
icon/decision icon/evidence icon/governance icon/hypothesis
icon/scope-boundary icon/succession-planning icon/target icon/tradeoff
''',
2: '''
icon/bottleneck icon/calendar icon/convergence icon/decomposition
icon/dependency icon/gradual-rollout icon/milestone icon/parallel-work
icon/priority icon/readiness-gate icon/work-queue icon/workflow
''',
3: '''
icon/calibration-reference icon/check icon/coverage icon/defect-isolation
icon/dimensional-measurement icon/feedback-loop icon/first-article-inspection icon/inspection
icon/leak-testing icon/material-traceability icon/measurement-tolerance icon/mistake-proofing
icon/pressure-test icon/quality icon/quality-sampling icon/rework
icon/scrap-disposal icon/tensile-test
''',
4: '''
icon/adhesive-bonding icon/adjustable-workbench icon/conveyor icon/drilling
icon/drying icon/fastening icon/filtration icon/gear
icon/humidity-control icon/load-capacity icon/manufacturing icon/material-cutting
icon/material-feeding icon/mixing icon/molding icon/preventive-maintenance
icon/process-cooling icon/process-heating icon/spare-parts icon/standard-work
icon/surface-finishing icon/temperature-control icon/tooling-changeover icon/vibration-monitoring
icon/weighing icon/welding
''',
5: '''
icon/buffer-stock icon/cold-chain icon/cross-docking icon/delivery
icon/delivery-deadline icon/flow-rack icon/inventory icon/loading-dock
icon/lot-identification icon/order-picking icon/package-sealing icon/pallet-handling
icon/pallet-stacking icon/procurement icon/returnable-container icon/returns
icon/warehouse
''',
6: '''
icon/automation icon/bill-of-materials icon/digital-twin icon/idea
icon/product-specification icon/sensor
''',
7: '''
icon/chemical-storage icon/electrical-grounding icon/electrostatic-control icon/emergency-eyewash
icon/emergency-stop icon/energy-isolation-lockout icon/evacuation-route icon/fall-protection
icon/fire-extinguisher icon/first-aid-kit icon/hazard-zone icon/hearing-protection
icon/incident icon/machine-guard icon/pedestrian-separation icon/protective-eyewear
icon/protective-gloves icon/resilience icon/respiratory-protection icon/risk
icon/safety-footwear icon/safety-helmet icon/shield icon/spill-containment
icon/ventilation
''',
8: '''
icon/air-filtration icon/biodiversity icon/daylight-use icon/emissions-measurement
icon/energy-efficiency icon/energy-storage icon/heat-recovery icon/material-recycling
icon/noise-reduction icon/oil-recovery icon/rainwater-harvesting icon/solar-power
icon/sustainability icon/waste-separation icon/wastewater-treatment icon/water-reuse
icon/wind-power
''',
9: '''
icon/accessibility icon/attendance icon/book icon/business-travel
icon/childcare-support icon/delegation icon/development icon/employee-wellbeing
icon/exit-interview icon/flexible-hours icon/knowledge-transfer icon/mentoring
icon/onboarding icon/payroll icon/performance icon/person
icon/professional-expertise icon/recruitment icon/remote-work icon/skill-matrix
icon/staff-transfer icon/team icon/visitor-reception icon/workload-balance
''',
10: '''
icon/after-sales-service icon/contract icon/customer icon/customer-feedback
icon/customer-support icon/demand-forecast icon/handshake icon/market-segmentation
icon/product-launch icon/quotation icon/sales-pipeline icon/service-renewal
icon/support-desk icon/survey
''',
11: '''
icon/break-even icon/budget icon/budget-allocation icon/capital-investment
icon/cash-flow icon/contingency-fund icon/cost-reduction icon/depreciation
icon/expense icon/foreign-exchange icon/invoice icon/payment
icon/profit-margin icon/tax
''',
12: '''
icon/access-control icon/access-protection icon/analytic-insight icon/analytics
icon/api icon/audit-trail icon/authentication icon/backup
icon/caching icon/cloud icon/connected-systems icon/data-cleansing
icon/data-lineage icon/data-retention icon/data-validation icon/database
icon/duplicate-removal icon/edge-processing icon/encryption icon/key
icon/laptop icon/monitoring icon/offline-mode icon/privacy
icon/rate-limit icon/routing icon/server icon/synchronization
icon/system-recovery icon/uncertainty icon/version-control icon/wireless-link
''',
13: '''
icon/approval icon/broadcast icon/conversation icon/document
icon/document-approval icon/download icon/email icon/globe
icon/meeting icon/notification icon/phone icon/presentation
icon/search icon/sharing icon/structured-report icon/upload
''',
}
for number,keys in ICON_GROUPS.items():GROUPS[number]=GROUPS.get(number,'')+' ' +keys
ASSIGNMENTS={key:LABELS[number] for number,keys in GROUPS.items() for key in keys.split()}
assert len(ASSIGNMENTS)==sum(len(keys.split()) for keys in GROUPS.values()),'Duplicate purpose assignments'


def category_for(key):
    if key in ASSIGNMENTS:return ASSIGNMENTS[key]
    namespace=key.split('/',1)[0]
    if namespace in NAMESPACES:return LABELS[NAMESPACES[namespace]]
    raise ValueError('Assign a primary purpose in scripts/categories.py: '+key)
