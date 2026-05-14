import React from 'react';
import { Pulse, AlertTriangle, TrendingUp, Clock } from 'lucide-react';

/**
 * SystemStatusDisplay 컴포넌트: 시스템 안정성 KPI를 시각적으로 표시합니다.
 * @param {object} props - 컴포넌트 속성
 * @param {number} props.errorRate - 오류율 (%)
 * @param {number} props.latency - 지연 시간 (ms)
 * @param {boolean} props.isStable - 시스템 안정 상태 (true: 정상, false: 경고/위험)
 */
const SystemStatusDisplay = ({ errorRate, latency, isStable }) => {
  // 1. 색상 및 상태 결정 로직
  let statusColor = 'text-green-500'; // 기본: 안정
  let icon = <TrendingUp className="w-6 h-6" />;
  let statusText = '시스템 정상';

  if (!isStable) {
    statusColor = 'text-red-500'; // 불안정/경고
    icon = <AlertTriangle className="w-6 h-6" />;
    statusText = '안정성 경고';
  } else if (errorRate > 1.0 || latency > 50) {
    statusColor = 'text-yellow-500'; // 주의 필요
    icon = <Pulse className="w-6 h-6" />;
    statusText = '주의: 성능 모니터링 필요';
  } else if (errorRate > 0.5 && latency > 100) {
    statusColor = 'text-orange-500'; // 위험 임계치 근접
    icon = <Pulse className="w-6 h-6" />;
    statusText = '위험: 지연 시간 증가';
  }

  // 2. 시각적 요소 구성 (레이아웃 좌표 및 스타일 반영)
  const containerStyle = {
    display: 'flex',
    alignItems: 'center',
    padding: '12px',
    borderRadius: '8px',
    borderLeft: `4px solid ${isStable ? '#10B981' : '#F59E0B'}`, // 녹색/주황 테두리 강조
    backgroundColor: isStable ? 'rgba(16, 185, 129, 0.05)' : 'rgba(245, 158, 11, 0.05)',
  };

  const detailStyle = {
    marginRight: '16px',
  };

  return (
    <div style={containerStyle}>
      {icon}
      <div style={detailStyle}>
        <span className={`text-lg font-semibold ${statusColor}`}>
          {statusText}
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{ marginRight: '8px', color: '#4B5563' }}>오류율 (Error Rate):</span>
        <span style={{ fontWeight: 'bold', color: isStable ? '#1F2937' : '#DC2626' }}>{errorRate.toFixed(2)}%</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <span style={{ marginRight: '8px', color: '#4B5563' }}>지연 시간 (Latency):</span>
        <span style={{ fontWeight: 'bold', color: isStable ? '#1F2937' : '#DC2626' }}>{latency.toFixed(2)}ms</span>
      </div>
    </div>
  );
};

export default SystemStatusDisplay;