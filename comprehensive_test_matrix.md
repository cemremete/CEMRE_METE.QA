# Comprehensive Test Case Matrix - Insider Onsite Experiment Pop-up

## Excel-Compatible Test Case Matrix

| Test ID | Category | Test Title | Manual Result | Automation Priority | Prerequisites | Test Steps | Expected Result | Bug ID (if any) | Severity | Browser Support | Mobile Support |
|---------|----------|------------|---------------|-------------------|---------------|------------|-----------------|-----------------|----------|-----------------|----------------|
| TC001 | Functional | Pop-up Display Test | FAIL | P1 | Browser open, test URL loaded | 1. Click "SHOW INSTANTLY" button | Pop-up displays successfully with English content | BUG001 | Critical | Chrome: FAIL, Firefox: FAIL, Safari: FAIL | Not Supported |
| TC002 | Functional | Pop-up Close via X Button | FAIL | P1 | Pop-up is displayed | 1. Click X button in top-right corner | Pop-up closes, main page visible | BUG008 | High | Chrome: FAIL | Not Supported |
| TC003 | Functional | Pop-up Close via Outside Click | FAIL | P1 | Pop-up is displayed | 1. Click outside pop-up area | Pop-up closes, main page visible | BUG008 | High | Chrome: FAIL | Not Supported |
| TC004 | Performance | Pop-up Load Performance | FAIL | P1 | Test panel open | 1. Click "SHOW INSTANTLY" 2. Measure load time | Pop-up loads within 2 seconds | BUG006 | High | Chrome: 4.49s delay | Not Tested |
| TC005 | Functional | Pop-up Content Validation | FAIL | P2 | Pop-up is displayed | 1. Verify pop-up content | English content displays correctly | BUG007 | Critical | Chrome: Wrong content | Not Supported |
| TC006 | Functional | Pop-up Re-display Test | PARTIAL | P2 | Pop-up was closed | 1. Click "SHOW INSTANTLY" again | Pop-up displays again successfully | - | Medium | Chrome: Partial | Not Supported |
| TC007 | Negative | Multiple Pop-up Prevention | NOT TESTED | P3 | Pop-up already open | 1. Click "SHOW INSTANTLY" again | No new pop-up opens, existing preserved | - | Low | Not Tested | Not Supported |
| TC008 | Negative | Pop-up State After Close | FAIL | P2 | Pop-up was closed | 1. Check pop-up elements in DOM | Pop-up elements not visible in DOM | BUG008 | High | Chrome: Elements remain | Not Supported |
| TC009 | Functional | Natural Pop-up Trigger Prevention | PASS | P2 | Browser open | 1. Navigate to Homepage 2. Wait 3. Navigate to Category 4. Wait 5. Navigate to Cart 6. Wait | Pop-up should NOT auto-trigger on these pages | - | Medium | Chrome: PASS | Not Supported |
| TC010 | Functional | Product-Popup Content Matching | FAIL | P1 | Product detail page | 1. Navigate to Mug product page 2. Trigger pop-up 3. Compare product names | Pop-up product matches page product | BUG007 | Critical | Chrome: 90% mismatch | Not Supported |
| TC011 | Edge Case | Rapid Open-Close Test | NOT TESTED | P3 | Test panel open | 1. Click "SHOW INSTANTLY" 2. Immediately click X | Pop-up opens and closes without error | - | Low | Not Tested | Not Supported |
| TC012 | Edge Case | Page Refresh During Pop-up | PASS | P3 | Pop-up is open | 1. Press F5 to refresh | Pop-up closes, page returns to normal | - | Low | Chrome: PASS | Not Supported |
| TC013 | UI/UX | Pop-up Visual Design | FAIL | P2 | Pop-up is displayed | 1. Verify pop-up design | Pop-up centered, appropriate size | BUG010 | High | Chrome: Design issues | Not Supported |
| TC014 | UI/UX | Pop-up Overlay Test | FAIL | P2 | Pop-up is displayed | 1. Check background overlay | Background darkened, pop-up in foreground | BUG010 | High | Chrome: No overlay | Not Supported |
| TC015 | Performance | Pop-up Open Speed | FAIL | P2 | Test panel open | 1. Click "SHOW INSTANTLY" 2. Measure open time | Pop-up opens within 1 second | BUG006 | High | Chrome: >1s delay | Not Supported |
| TC016 | Performance | Pop-up Close Speed | FAIL | P3 | Pop-up is open | 1. Click X button 2. Measure close time | Pop-up closes within 0.5 seconds | BUG008 | Medium | Chrome: Slow close | Not Supported |
| TC017 | Browser Compatibility | Chrome Browser Test | FAIL | P1 | Chrome browser | 1. Test all pop-up functions | All features work in Chrome | BUG001, BUG002 | Critical | Chrome: Multiple failures | Not Supported |
| TC018 | Browser Compatibility | Firefox Browser Test | FAIL | P1 | Firefox browser | 1. Test all pop-up functions | All features work in Firefox | BUG005 | Critical | Firefox: Complete failure | Not Supported |
| TC019 | Browser Compatibility | Safari Browser Test | FAIL | P1 | Safari browser | 1. Test all pop-up functions | All features work in Safari | BUG005 | Critical | Safari: Complete failure | Not Supported |
| TC020 | Responsive | Mobile View Test | FAIL | P1 | Mobile device/emulator | 1. Test pop-up on mobile | Pop-up displays properly on mobile | BUG004 | Critical | Not Supported | 0% functionality |
| TC021 | Responsive | Tablet View Test | FAIL | P1 | Tablet device/emulator | 1. Test pop-up on tablet | Pop-up displays properly on tablet | BUG004 | Critical | Not Supported | 0% functionality |
| TC022 | Accessibility | Keyboard Navigation | NOT TESTED | P3 | Pop-up is open | 1. Use Tab key 2. Try Enter to close | Pop-up closable via keyboard | - | Low | Not Tested | Not Supported |
| TC023 | Business Critical | Add to Cart Functionality | FAIL | P1 | Pop-up with product | 1. Click "Add to Cart" in pop-up | Product added to cart successfully | BUG002 | Critical | Chrome: Button not working | Not Supported |
| TC024 | Business Critical | Price Display Accuracy | FAIL | P1 | Pop-up with product | 1. Compare pop-up price with product page | Prices match, discounts applied correctly | BUG003 | Critical | Chrome: Price errors | Not Supported |
| TC025 | Memory | Memory Leak Test | FAIL | P2 | Multiple pop-up cycles | 1. Open/close pop-up 50 times 2. Monitor memory | No significant memory increase | BUG009 | High | Chrome: Memory leak detected | Not Supported |

## Test Results Summary by Category

### Functional Tests (9 tests)
- **PASS:** 1 test (11.1%)
- **FAIL:** 7 tests (77.8%)
- **PARTIAL:** 1 test (11.1%)

### Performance Tests (3 tests)
- **PASS:** 0 tests (0%)
- **FAIL:** 3 tests (100%)

### Browser Compatibility Tests (3 tests)
- **PASS:** 0 tests (0%)
- **FAIL:** 3 tests (100%)

### Responsive Tests (2 tests)
- **PASS:** 0 tests (0%)
- **FAIL:** 2 tests (100%)

### Business Critical Tests (2 tests)
- **PASS:** 0 tests (0%)
- **FAIL:** 2 tests (100%)

### UI/UX Tests (2 tests)
- **PASS:** 0 tests (0%)
- **FAIL:** 2 tests (100%)

### Edge Case Tests (2 tests)
- **PASS:** 1 test (50%)
- **NOT TESTED:** 1 test (50%)

### Negative Tests (2 tests)
- **FAIL:** 1 test (50%)
- **NOT TESTED:** 1 test (50%)

### Accessibility Tests (1 test)
- **NOT TESTED:** 1 test (100%)

### Memory Tests (1 test)
- **FAIL:** 1 test (100%)

## Automation Priority Matrix

### P1 (Critical - Immediate Automation) - 12 tests
- TC001: Pop-up Display Test
- TC002: Pop-up Close via X Button  
- TC003: Pop-up Close via Outside Click
- TC004: Pop-up Load Performance
- TC010: Product-Popup Content Matching
- TC017: Chrome Browser Test
- TC018: Firefox Browser Test
- TC019: Safari Browser Test
- TC020: Mobile View Test
- TC021: Tablet View Test
- TC023: Add to Cart Functionality
- TC024: Price Display Accuracy

### P2 (High - Next Sprint) - 8 tests
- TC005: Pop-up Content Validation
- TC006: Pop-up Re-display Test
- TC008: Pop-up State After Close
- TC009: Natural Pop-up Trigger Prevention
- TC013: Pop-up Visual Design
- TC014: Pop-up Overlay Test
- TC015: Pop-up Open Speed
- TC025: Memory Leak Test

### P3 (Medium - Future Releases) - 5 tests
- TC007: Multiple Pop-up Prevention
- TC011: Rapid Open-Close Test
- TC012: Page Refresh During Pop-up
- TC016: Pop-up Close Speed
- TC022: Keyboard Navigation

## Production Readiness Assessment

### 🚨 RECOMMENDATION: NO-GO FOR PRODUCTION

### Critical Blockers:
1. **Core Functionality Broken:** Add to Cart button non-functional (BUG002)
2. **Cross-Browser Failure:** Firefox and Safari completely non-functional (BUG005)
3. **Mobile Incompatibility:** 0% mobile/tablet functionality (BUG004)
4. **Content Accuracy:** 90% incorrect product mapping (BUG007)
5. **Performance Issues:** 4.49s load time exceeds 2s standard (BUG006)

### Minimum Go-Live Requirements:
- [ ] Fix Add to Cart functionality (BUG002)
- [ ] Implement responsive design for mobile/tablet (BUG004)
- [ ] Fix Firefox/Safari compatibility (BUG005)
- [ ] Reduce load time to <2 seconds (BUG006)
- [ ] Fix content mapping accuracy to >95% (BUG007)
- [ ] Implement proper pop-up close functionality (BUG008)
- [ ] Add background overlay (BUG010)

### Success Criteria for Production:
- **Functional Success Rate:** >90% (Currently: 22.9%)
- **Cross-Browser Support:** Chrome, Firefox, Safari working
- **Mobile Support:** Responsive design implemented
- **Performance:** <2s load time
- **Content Accuracy:** >95% correct product mapping