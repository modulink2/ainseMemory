import React, { useState } from 'react';

// --- Color Palette Definition (Based on Designer Guidelines) ---
const COLORS = {
  NAVY_BLUE: '#0A1931', // Primary Background
  SYSTEM_GREEN: '#4CAF50', // Stability Indicator (PTI Green)
  RED_ALERT: '#F44336',   // Risk Alert (Safe Mode)
  TEXT_LIGHT: '#E0E0E0', // Text/Accent
};

// --- Mock Data for Demonstration ---
const mockData = {
  pti: 98.5, // System Stability Index (PTI)
  roi: 1.25, // Return on Investment
  safeMode: false,
  status: "System Stable",
};

// --- Core Dashboard Component ---
const DashboardPrototype = () => {
  const [data, setData] = useState(mockData);

  // Dynamic color based on PTI status
  const ptiColor = data.pti >= 90 ? COLORS.SYSTEM_GREEN : COLORS.RED_ALERT;
  const headerBg = data.safeMode ? COLORS.RED_ALERT + '20' : COLORS.NAVY_BLUE; // Subtle background change for alert

  return (
    <div style={{ backgroundColor: COLORS.NAVY_BLUE, minHeight: '100vh', color: COLORS.TEXT_LIGHT, fontFamily: 'Arial, sans-serif' }}>
      
      {/* A. 최상단 시스템 상태 표시줄 (PTI Emphasis) */}
      <header style={{ 
        backgroundColor: headerBg, 
        padding: '20px', 
        textAlign: 'center', 
        borderBottom: `4px solid ${ptiColor}` 
      }}>
        <h1>갓더주식 대시보드</h1>
        <div style={{ fontSize: '3em', fontWeight: 'bold', color: ptiColor, margin: '10px 0' }}>
          PTI: {data.pti.toFixed(2)}
        </div>
        <p style={{ color: data.safeMode ? COLORS.RED_ALERT : COLORS.SYSTEM_GREEN, fontWeight: 'bold' }}>
          상태: {data.status}
        </p>
      </header>

      {/* B. 메인 대시보드 영역 */}
      <main style={{ padding: '30px' }}>
        <h2>투자 성과 요약</h2>
        
        {/* KPI Card 1: PTI (Most Prominent) */}
        <div style={{ 
          backgroundColor: '#1A2B47', // Slightly lighter than background
          padding: '25px', 
          borderRadius: '10px', 
          marginBottom: '20px',
          borderLeft: `5px solid ${ptiColor}` // Green border emphasis
        }}>
          <h3>시스템 안정성 지수 (PTI)</h3>
          <p style={{ fontSize: '3em', margin: '5px 0' }}>{data.pti.toFixed(2)}</p>
          <p>안정성이 곧 수익입니다.</p>
        </div>

        {/* KPI Card 2: ROI */}
        <div style={{ 
          backgroundColor: '#1A2B47', 
          padding: '25px', 
          borderRadius: '10px', 
          borderLeft: `5px solid ${data.pti >= 90 ? COLORS.SYSTEM_GREEN : COLORS.RED_ALERT}`
        }}>
          <h3>투자 수익률 (ROI)</h3>
          <p style={{ fontSize: '3em', margin: '5px 0' }}>{data.roi.toFixed(2)}</p>
          <p>현재 시장 대비 성과 지표.</p>
        </div>

        {/* C. 리스크 섹션 */}
        <div style={{ marginTop: '30px', padding: '20px', borderRadius: '10px' }}>
          <h3>리스크 제어 상태</h3>
          {!data.safeMode ? (
            <p style={{ color: COLORS.SYSTEM_GREEN, fontSize: '1.2em', fontWeight: 'bold' }}>
              ✅ 안전 모드 해제됨 (System Stable)
            </p>
          ) : (
            <p style={{ color: COLORS.RED_ALERT, fontSize: '1.2em', fontWeight: 'bold' }}>
              🚨 **경고: 안전 모드 활성화됨** - 자동매매 일시 정지
            </p>
          )}
        </div>

      </main>
    </div>
  );
};

export default DashboardPrototype;