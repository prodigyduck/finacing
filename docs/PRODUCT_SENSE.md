# Product Sense

## Overview

This document defines the product vision, user value proposition, and strategic positioning of the Financing project. It articulates why this product exists, who it serves, and what makes it unique.

---

## Product Vision

**To democratize investment portfolio management by providing a simple, yet powerful tool for individual investors to track, analyze, and optimize their investments.**

We believe everyone deserves access to sophisticated portfolio analytics without the complexity and cost of enterprise-grade financial tools.

---

## Mission Statement

**Empower individual investors with data-driven insights to make informed investment decisions.**

We achieve this by:
- Simplifying investment tracking through intuitive interfaces
- Providing actionable analytics without overwhelming users
- Leveraging local-first tools users already use (Obsidian)
- Maintaining absolute privacy by keeping data on the user's machine

---

## Problem Statement

### The Problem

Individual investors face several challenges:

1. **Fragmented Data:** Investments spread across multiple platforms (brokerage accounts, retirement funds, crypto exchanges)
2. **Manual Tracking:** Excel spreadsheets and manual calculations are time-consuming and error-prone
3. **Limited Insights:** Basic trading platforms provide little analytical depth
4. **Complex Tools:** Enterprise financial software is overkill for individual needs
5. **High Cost:** Professional portfolio management tools are expensive
6. **Data Privacy:** Reluctance to share sensitive financial data with third-party services

### The Impact

- Poor visibility into overall financial health
- Suboptimal asset allocation decisions
- Missed opportunities for portfolio optimization
- Increased risk due to lack of diversification analysis
- Time wasted on manual data aggregation

---

## Solution

### Our Approach

Financing addresses these problems by:

1. **Local-First Architecture:** Use Obsidian, a local-first markdown tool many already use for notes
2. **Simple Data Entry:** Natural language parsing for investment records (M.DD format)
3. **Automated Analytics:** Real-time portfolio calculations and visualizations
4. **Absolute Privacy:** Data stays on the user's machine in local Obsidian vault, never sent to external servers
5. **Zero Learning Curve:** Intuitive interface, no financial expertise required
6. **Free to Use:** Open-source, no subscription fees

---

## Target Audience

### Primary Users

**Individual Investors (25-55 years old)**

**Characteristics:**
- Have multiple investment accounts
- Manage portfolios themselves (self-directed investors)
- Tech-savvy, comfortable with web applications
- Value privacy and data control
- Want better insights without enterprise complexity

**Use Cases:**
- Track portfolio performance across multiple platforms
- Understand asset allocation and diversification
- Calculate returns and performance metrics
- Make informed rebalancing decisions

### Secondary Users

**Retirement Planners**
- Individuals planning for retirement
- Need long-term portfolio tracking
- Want to monitor progress toward financial goals

**Financial Literacy Learners**
- Beginners learning about investing
- Want to understand portfolio composition
- Need visual representation of concepts

---

## User Value Proposition

### Core Benefits

1. **Time Savings**
   - No more manual spreadsheets
   - Automated calculations
   - One-click portfolio updates
   - **Value:** Save 2-5 hours per week

2. **Better Decisions**
   - Real-time portfolio analytics
   - Asset allocation visualization
   - Performance metrics at a glance
   - **Value:** Make data-driven investment decisions

3. **Risk Management**
   - Diversification analysis
   - Concentration risk alerts
   - Performance attribution
   - **Value:** Reduce portfolio risk through awareness

4. **Privacy & Control**
   - Data in your local Obsidian vault
   - No account required
   - No data sent to external servers
   - No credentials to manage
   - **Value:** Complete privacy and data ownership

5. **Accessibility**
   - Free and open-source
   - Simple, intuitive interface
   - Works on any device with browser
   - **Value:** Professional tools, zero cost

---

## Differentiation

### vs. Spreadsheets (Excel, Google Sheets)

| Feature | Financing | Spreadsheets |
|---------|-----------|--------------|
| Automated Calculations | Yes | No (Manual) |
| Visualizations | Yes | Partial (Manual setup) |
| Real-time Updates | Yes | No |
| Error-prone | No | Yes |
| Data Entry | Natural format (M.DD) | Structured format |
| Privacy | Local files | Cloud-based |

**Why Financing Wins:** Automation, accuracy, and ease of use

---

### vs. Trading Platform Dashboards

| Feature | Financing | Trading Platforms |
|---------|-----------|-------------------|
| Multi-Account | Yes | No (Single platform) |
| Deep Analytics | Yes | Partial (Basic) |
| Privacy | Yes (Your local data) | No (Platform data) |
| Customization | Yes | No |
| Cost | Free | Subscription-based |
| Learning Curve | Low | Medium |

**Why Financing Wins:** Consolidated view, privacy, and cost

---

### vs. Enterprise Portfolio Management Tools

| Feature | Financing | Enterprise Tools |
|---------|-----------|------------------|
| Complexity | Low | High |
| Cost | Free | $100+/month |
| Target User | Individual | Professional |
| Setup Time | 5 minutes | Hours/Days |
| Features | Focused | Comprehensive |
| Deployment | Personal | Enterprise |

**Why Financing Wins:** Simplicity, speed, and cost for individual needs

---

## User Journey

### Onboarding Flow

1. **Discovery**
   - User hears about Financing through word-of-mouth or open-source community
   - User visits GitHub repository or documentation

2. **Installation**
   - User clones repository or downloads application
   - User runs installation commands
   - User configures Obsidian vault path (default: ~/git/obsidian/투자/투자.md)

3. **First Use**
   - User ensures investment data exists in Obsidian vault (M.DD format)
   - User views dashboard with parsed data
   - User explores visualizations and analytics

4. **Adoption**
   - User adds more investment records to Obsidian
   - User sets up regular portfolio reviews
   - User discovers insights about portfolio

5. **Habit Formation**
   - User checks dashboard regularly
   - User makes informed investment decisions
   - User recommends to others

### Key Moments

**Aha Moment:** First time user sees portfolio visualized automatically from a simple markdown file

**Habit Formation:** Regular dashboard checks become part of investment routine

**Advocacy:** User recommends to other investors due to simplicity, privacy, and value

---

## Success Metrics

### Product Metrics

**Acquisition:**
- Monthly active users (MAU)
- New user sign-ups (if multi-user)
- GitHub stars and forks

**Engagement:**
- Daily active users (DAU)
- Average session duration
- Feature usage rates
- Dashboard refresh frequency

**Retention:**
- 7-day retention
- 30-day retention
- 90-day retention
- Churn rate

**Satisfaction:**
- Net Promoter Score (NPS)
- User satisfaction surveys
- Feature request feedback
- Bug reports and issue resolution time

### Business Metrics (Future)

**If Monetized:**
- Conversion rate (free -> paid)
- Average revenue per user (ARPU)
- Customer acquisition cost (CAC)
- Lifetime value (LTV)

---

## Product Philosophy

### Design Principles

1. **Simplicity First**
   - Complex problems, simple solutions
   - Minimal cognitive load
   - Intuitive user experience

2. **Privacy by Design**
   - User-controlled data on local machine
   - No unnecessary data collection
   - No external API dependencies for core data
   - Transparent data handling

3. **Progressive Disclosure**
   - Start simple, reveal complexity when needed
   - Avoid overwhelming new users
   - Provide advanced features for power users

4. **Actionable Insights**
   - Don't just show data, provide insights
   - Help users make decisions
   - Contextualize information

5. **Continuous Improvement**
   - Listen to user feedback
   - Iterate quickly
   - Measure impact of changes

---

## Competitive Advantage

### Technical Advantages

1. **Clean Architecture**
   - Maintainable codebase
   - Easy to extend
   - Testable components

2. **Local-First Design**
   - Data stays on user's machine
   - No centralized database
   - GDPR-friendly by nature
   - No external API dependencies

3. **Open Source**
   - Community contributions
   - Transparent development
   - Customizable

### Business Advantages

1. **Low Barrier to Entry**
   - Free to use
   - Simple setup (just point to Obsidian vault)
   - No account required
   - No credentials to manage

2. **Niche Focus**
   - Individual investors
   - Korean market (initially)
   - Obsidian local-first integration

3. **Community-Led**
   - User-driven features
   - Word-of-mouth growth
   - Organic adoption

---

## Future Vision

### Phase 1: Foundation (Current)
- Core portfolio tracking
- Basic analytics
- Obsidian vault data reading
- Single-user support
- FastAPI backend

### Phase 2: Enhanced Analytics (3-6 months)
- Historical performance tracking
- Risk analysis
- Portfolio optimization
- Advanced visualizations

### Phase 3: Platform Expansion (6-12 months)
- Multi-user support
- Multiple data sources
- Mobile application
- Full REST API

### Phase 4: Ecosystem (12+ months)
- Third-party integrations
- Marketplace for plugins
- Community features
- Professional version

---

## Risks & Mitigation

### Product Risks

**Risk:** Low user adoption
**Mitigation:**
- Focus on word-of-mouth and community growth
- Improve onboarding experience
- Gather and act on user feedback

**Risk:** Obsidian vault format changes
**Mitigation:**
- Implement flexible parser with format validation
- Support multiple file formats
- Provide data migration tools

**Risk:** Competition from larger platforms
**Mitigation:**
- Focus on niche use case
- Maintain simplicity and privacy advantage
- Leverage open-source community

---

## Success Stories (Future)

### Example 1: The Busy Professional

**Problem:** Kim, 35, works long hours and hasn't reviewed her portfolio in months

**Solution:** Financing automated tracking gave her a clear view in 5 minutes from her Obsidian notes

**Outcome:** Rebalanced portfolio, reduced concentration risk, better returns

---

### Example 2: The Retirement Planner

**Problem:** Lee, 50, planning retirement, unsure if on track

**Solution:** Financing historical tracking showed consistent progress from vault records

**Outcome:** Confident retirement plan, adjusted savings rate appropriately

---

### Example 3: The Beginning Investor

**Problem:** Park, 28, new to investing, overwhelmed by data

**Solution:** Financing simple interface made portfolio understandable from daily Obsidian notes

**Outcome:** Better understanding, more confident decisions, continued investing

---

## Brand Voice

**Personality:**
- Helpful and supportive
- Knowledgeable but approachable
- Transparent and trustworthy
- Innovative yet practical

**Tone:**
- Clear and concise
- Avoids jargon
- Encouraging and positive
- Respectful of user intelligence

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-04-19 | Updated for Obsidian local-first architecture |
| 1.0.0 | 2026-03-29 | Initial product sense documentation |
