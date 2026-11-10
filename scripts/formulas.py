# Key formulas typed as plain text in the Google Docs notes, rewritten as LaTeX.
# chapter -> list of (exact line after pandoc conversion, replacement Markdown).
# Worked numerical examples are left as text on purpose.
# A line that no longer matches (because the docx changed) is reported by
# docx_to_qmd.py, and the plain text is kept as it was.

FORMULAS = {
    3: [
        ("  - ROE는 자금조달 구조의 영향을 받는다. **ROE = ROIC + (부채/자본) × \\[ROIC − 세후 이자율\\]**로 쓸 수 있다.",
         "  - ROE는 자금조달 구조의 영향을 받는다. 다음과 같이 쓸 수 있다.\n\n    $$\\text{ROE} = \\text{ROIC} + \\frac{D}{E}\\,\\big[\\text{ROIC} - i\\,(1-t)\\big]$$\n\n    ($i\\,(1-t)$: 세후 이자율)"),
    ],
    4: [
        ("- 포트폴리오 분산 = wₐ²σₐ² + (1−wₐ)²σ_b² + 2wₐ(1−wₐ)ρₐ_bσₐσ_b",
         "- 포트폴리오 분산:\n\n  $$\\sigma_p^2 = w_a^2\\sigma_a^2 + (1-w_a)^2\\sigma_b^2 + 2w_a(1-w_a)\\rho_{ab}\\sigma_a\\sigma_b$$"),
        ("  - 베타 = 자산과 시장의 공분산 ÷ 시장의 분산",
         "  - 베타 = 자산과 시장의 공분산 ÷ 시장의 분산: $\\beta_i = \\dfrac{\\mathrm{Cov}(R_i, R_m)}{\\sigma_m^2}$"),
        ("- **기대수익률**: **E(R) = 무위험이자율 + 베타 × \\[시장 기대수익률 − 무위험이자율\\]**",
         "- **기대수익률**:\n\n  $$E(R_i) = R_f + \\beta_i\\,\\big[E(R_m) - R_f\\big]$$"),
        ("- **E(R) = 무위험이자율 + β₁\\[요인 1 프리미엄\\] + β₂\\[요인 2 프리미엄\\] + ...** CAPM은 요인이 하나(시장 포트폴리오)뿐인 특수한 경우다.",
         "- 다요인 기대수익률:\n\n  $$E(R) = R_f + \\beta_1\\,[\\text{요인 1 프리미엄}] + \\beta_2\\,[\\text{요인 2 프리미엄}] + \\cdots$$\n\n  CAPM은 요인이 하나(시장 포트폴리오)뿐인 특수한 경우다."),
    ],
    5: [
        ("  - Δ(옵션 델타) = (Cu − Cd) / (Su − Sd)",
         "  - 옵션 델타: $\\Delta = \\dfrac{C_u - C_d}{S_u - S_d}$"),
        ("  - 옵션 가치 = Δ × S − B",
         "  - 옵션 가치: $C = \\Delta S - B$"),
        ("- **콜 가치** C = S·N(d1) − K·e\\^(−rt)·N(d2)",
         "- **콜 가치**\n\n  $$C = S\\,N(d_1) - K e^{-rt} N(d_2)$$"),
        ("  - d1 = \\[ln(S/K) + (r + σ²/2)t\\] / (σ√t), d2 = d1 − σ√t",
         "  - $d_1 = \\dfrac{\\ln(S/K) + (r + \\sigma^2/2)\\,t}{\\sigma\\sqrt{t}}, \\quad d_2 = d_1 - \\sigma\\sqrt{t}$"),
        ("  - C = S·e\\^(−yt)·N(d1) − K·e\\^(−rt)·N(d2), d1 = \\[ln(S/K) + (r − y + σ²/2)t\\] / (σ√t)",
         "  - 배당수익률 $y$ 반영:\n\n    $$C = S e^{-yt} N(d_1) - K e^{-rt} N(d_2), \\qquad d_1 = \\frac{\\ln(S/K) + (r - y + \\sigma^2/2)\\,t}{\\sigma\\sqrt{t}}$$"),
        ("- u = exp\\[σ√dt + (r − σ²/2)dt\\], d = exp\\[−σ√dt + (r − σ²/2)dt\\]",
         "- $u = \\exp\\!\\big[\\sigma\\sqrt{dt} + (r - \\sigma^2/2)\\,dt\\big], \\quad d = \\exp\\!\\big[-\\sigma\\sqrt{dt} + (r - \\sigma^2/2)\\,dt\\big]$"),
        ("- 희석 조정 주가 S = (S·ns + W·nw) / (ns + nw)",
         "- 희석 조정 주가: $S_{adj} = \\dfrac{S\\,n_s + W\\,n_w}{n_s + n_w}$"),
        ("  - S + P − C = K·e\\^(−rt) → **C − P = S − K·e\\^(−rt)**",
         "  - $S + P - C = K e^{-rt}$ 이므로\n\n    $$C - P = S - K e^{-rt}$$"),
        ("- 이를 이용한 풋 가치: P = K·e\\^(−rt)\\[1 − N(d2)\\] − S·e\\^(−yt)\\[1 − N(d1)\\]",
         "- 이를 이용한 풋 가치:\n\n  $$P = K e^{-rt}\\,[1 - N(d_2)] - S e^{-yt}\\,[1 - N(d_1)]$$"),
    ],
    7: [
        ("- 앞의 세 모형: **E(R) = Rf + Σ βj × (위험프리미엄j)**. CAPM에서는 요인이 하나(시장)뿐이다.",
         "- 앞의 세 모형:\n\n  $$E(R) = R_f + \\sum_j \\beta_j \\times \\text{위험프리미엄}_j$$\n\n  CAPM에서는 요인이 하나(시장)뿐이다."),
        ("**ERP(국가) = ERP(성숙 시장) + 국가위험프리미엄**",
         "$$\\text{ERP}_{\\text{국가}} = \\text{ERP}_{\\text{성숙 시장}} + \\text{CRP}$$"),
        ("- 상대 표준편차 = σ(해당국 주식) / σ(미국 주식), ERP(해당국) = ERP(미국) × 상대 표준편차",
         "- 상대 표준편차를 이용:\n\n  $$\\text{ERP}_{\\text{해당국}} = \\text{ERP}_{\\text{미국}} \\times \\frac{\\sigma_{\\text{해당국 주식}}}{\\sigma_{\\text{미국 주식}}}$$"),
        ("- CRP = 국가 부도스프레드 × (σ주식 / σ국채)",
         "- 국가위험프리미엄:\n\n  $$\\text{CRP} = \\text{국가 부도스프레드} \\times \\frac{\\sigma_{\\text{주식}}}{\\sigma_{\\text{국채}}}$$"),
    ],
    8: [
        ("- 주식 수익률을 시장지수 수익률에 회귀한다: **Rj = a + b·Rm**",
         "- 주식 수익률을 시장지수 수익률에 회귀한다: $R_j = a + b\\,R_m$"),
        ("  - **기울기 b = 베타** = Cov(Rj, Rm)/σm²",
         "  - **기울기 b = 베타**: $b = \\dfrac{\\mathrm{Cov}(R_j, R_m)}{\\sigma_m^2}$"),
        ("**βL = βU × \\[1 + (1 − t) × (D/E)\\]**",
         "$$\\beta_L = \\beta_U\\,\\big[1 + (1 - t)\\,(D/E)\\big]$$"),
        ("**세후 부채비용 = (무위험이자율 + 부도스프레드) × (1 − 세율)**",
         "$$k_d^{\\text{세후}} = (R_f + \\text{부도스프레드})\\,(1 - t)$$"),
        ("**WACC = ke × E/(D+E+PS) + kd × D/(D+E+PS) + kps × PS/(D+E+PS)** (모두 시장가치)",
         "$$\\text{WACC} = k_e\\frac{E}{D+E+PS} + k_d\\frac{D}{D+E+PS} + k_{ps}\\frac{PS}{D+E+PS}$$\n\n(모두 시장가치)"),
    ],
}
