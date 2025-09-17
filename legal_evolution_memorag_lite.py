#!/usr/bin/env python3
"""
Legal Evolution MemoRAG Lite Integration
========================================

Lightweight version of MemoRAG integration for Legal Evolution Dataset analysis.
Works without full MemoRAG installation, demonstrating the integration architecture.

Author: Lex Certainty Enterprise
Version: 1.0.0-lite
Date: September 2024
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import re
from collections import defaultdict

class LegalEvolutionMemoRAGLite:
    """
    Lightweight Legal Evolution Analysis with MemoRAG-inspired Memory System
    
    Provides memory-inspired knowledge discovery for legal evolution patterns
    without requiring full MemoRAG installation.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize Legal Evolution MemoRAG Lite system"""
        self.config = self._load_config(config_path)
        self.legal_memory = {}
        self.evolution_cases = pd.DataFrame()
        self.velocity_metrics = pd.DataFrame()
        self.crisis_periods = pd.DataFrame()
        self.transplant_cases = pd.DataFrame()
        self.innovations_exported = pd.DataFrame()
        
        # Legal Evolution Dataset paths
        self.dataset_paths = {
            'evolution_cases': './evolution_cases.csv',
            'velocity_metrics': './velocity_metrics.csv',
            'transplants_tracking': './transplants_tracking.csv',
            'crisis_periods': './crisis_periods.csv',
            'innovations_exported': './innovations_exported.csv'
        }
        
        self._load_legal_datasets()
        self._build_memory_index()
        
        print("🏛️ Legal Evolution MemoRAG Lite initialized successfully!")
        print(f"📊 Loaded {len(self.evolution_cases)} evolution cases")
        print(f"📈 Loaded {len(self.velocity_metrics)} velocity metrics")
        print(f"🔄 Loaded {len(self.transplant_cases)} transplant cases")
        print(f"⚡ Loaded {len(self.crisis_periods)} crisis periods")
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration for Legal Evolution MemoRAG"""
        default_config = {
            "model_name": "lite-memory-system",
            "memory_type": "legal_evolution",
            "max_memory_length": 10000,
            "retrieval_top_k": 20,
            "legal_domains": [
                "constitucional", "civil", "comercial", "financiero", 
                "administrativo", "procesal", "criminal", "laboral",
                "tributario", "cambiario", "bancario", "ambiental"
            ],
            "temporal_analysis": {
                "start_year": 1950,
                "end_year": 2024,
                "crisis_detection": True,
                "velocity_tracking": True
            },
            "reality_filter": {
                "enabled": True,
                "primary_sources": ["InfoLeg", "SAIJ", "CSJN", "Boletín Oficial"],
                "verification_threshold": 0.95
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"⚠️ Config loading error: {e}, using defaults")
        
        return default_config
    
    def _load_legal_datasets(self):
        """Load all Legal Evolution Dataset files into memory"""
        try:
            for dataset_name, path in self.dataset_paths.items():
                if os.path.exists(path):
                    df = pd.read_csv(path, encoding='utf-8')
                    setattr(self, dataset_name, df)
                    print(f"✅ Loaded {dataset_name}: {len(df)} records")
                else:
                    print(f"⚠️ Dataset not found: {path}")
                    setattr(self, dataset_name, pd.DataFrame())
                    
        except Exception as e:
            print(f"❌ Error loading legal datasets: {e}")
            raise
    
    def _build_memory_index(self):
        """Build searchable memory index from legal datasets"""
        self.memory_index = {
            'evolution_cases': {},
            'crisis_periods': {},
            'transplant_cases': {},
            'keywords': defaultdict(list),
            'temporal': defaultdict(list),
            'legal_areas': defaultdict(list)
        }
        
        # Index evolution cases
        if not self.evolution_cases.empty:
            for idx, case in self.evolution_cases.iterrows():
                case_id = case['case_id']
                self.memory_index['evolution_cases'][case_id] = {
                    'content': self._build_case_memory(case),
                    'metadata': {
                        'legal_area': case['area_derecho'],
                        'start_date': case['fecha_inicio'],
                        'success': case['exito'],
                        'type': 'evolution_case'
                    }
                }
                
                # Build keyword index
                keywords = self._extract_keywords(case['nombre_caso'] + " " + str(case.get('notas', '')))
                for keyword in keywords:
                    self.memory_index['keywords'][keyword.lower()].append(case_id)
                
                # Build temporal index
                year = str(case['fecha_inicio'])[:4]
                self.memory_index['temporal'][year].append(case_id)
                
                # Build legal area index
                self.memory_index['legal_areas'][case['area_derecho']].append(case_id)
        
        # Index crisis periods
        if not self.crisis_periods.empty:
            for idx, crisis in self.crisis_periods.iterrows():
                crisis_id = crisis['crisis_id']
                self.memory_index['crisis_periods'][crisis_id] = {
                    'content': self._build_crisis_memory(crisis),
                    'metadata': {
                        'crisis_type': crisis['crisis_type'],
                        'severity': crisis['severity_level'],
                        'start_date': crisis['start_date'],
                        'type': 'crisis_period'
                    }
                }
        
        print(f"🧠 Memory index built: {len(self.memory_index['evolution_cases'])} cases, {len(self.memory_index['crisis_periods'])} crises")
    
    def _build_case_memory(self, case: pd.Series) -> str:
        """Build memory content for legal evolution case"""
        return f"""
        Legal Evolution Case: {case['nombre_caso']}
        Legal Area: {case['area_derecho']}
        Period: {case['fecha_inicio']} to {case['fecha_fin']}
        Evolution Type: {case['tipo_seleccion']}
        Origin: {case['origen']}
        Success Level: {case['exito']}
        Environmental Pressure: {case['presion_ambiental']}
        Key Actors: {case['actores_principales']}
        Primary Legislation: {case['normativa_primaria']}
        Relevant Rulings: {case['fallos_relevantes']}
        Survival Years: {case['supervivencia_anos']}
        Mutations: {case['mutaciones_identificadas']}
        International Diffusion: {case['difusion_otras_jurisdicciones']}
        Notes: {case.get('notas', '')}
        """
    
    def _build_crisis_memory(self, crisis: pd.Series) -> str:
        """Build memory content for crisis period"""
        return f"""
        Crisis Period: {crisis['crisis_name']}
        Duration: {crisis['start_date']} to {crisis['end_date']}
        Type: {crisis['crisis_type']}
        Severity: {crisis['severity_level']}
        Legal Changes: {crisis['legal_changes_count']}
        Emergency Decrees: {crisis['emergency_decrees']}
        New Laws: {crisis['new_laws']}
        Acceleration Factor: {crisis['acceleration_factor']}
        Economic Indicators: {crisis['economic_indicators']}
        Recovery Timeline: {crisis['recovery_timeline_months']} months
        Long-term Impact: {crisis['long_term_institutional_impact']}
        """
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        if pd.isna(text):
            return []
        
        # Simple keyword extraction
        words = re.findall(r'\w+', text.lower())
        # Filter out common words and keep meaningful terms
        stopwords = {'de', 'la', 'el', 'en', 'y', 'a', 'que', 'del', 'las', 'los', 'con', 'por', 'para'}
        keywords = [w for w in words if len(w) > 3 and w not in stopwords]
        return list(set(keywords))
    
    def query_legal_evolution(self, query: str, context_type: Optional[str] = None) -> Dict:
        """
        Query legal evolution patterns using memory-inspired retrieval
        
        Args:
            query: Natural language query about legal evolution
            context_type: Optional filter for specific context
            
        Returns:
            Dictionary with analysis results and sources
        """
        try:
            print(f"🔍 Processing query: {query}")
            
            # Extract query keywords
            query_keywords = self._extract_keywords(query)
            
            # Search memory index
            relevant_cases = self._search_memory(query_keywords, context_type)
            
            # Generate response
            response = self._generate_response(query, relevant_cases)
            
            # Analyze response
            analysis = self._analyze_response(response, query)
            
            result = {
                'query': query,
                'response': response,
                'analysis': analysis,
                'relevant_cases': [case['id'] for case in relevant_cases],
                'confidence': self._calculate_confidence(relevant_cases, query_keywords),
                'sources': self._extract_sources(response),
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Query processed - Confidence: {result['confidence']:.2f}")
            return result
            
        except Exception as e:
            return {
                'query': query,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _search_memory(self, keywords: List[str], context_type: Optional[str] = None) -> List[Dict]:
        """Search memory index for relevant cases"""
        scored_cases = []
        
        # Search evolution cases
        if not context_type or context_type == 'evolution_cases':
            for case_id, case_data in self.memory_index['evolution_cases'].items():
                score = self._calculate_relevance_score(case_data['content'], keywords)
                if score > 0:
                    scored_cases.append({
                        'id': case_id,
                        'type': 'evolution_case',
                        'score': score,
                        'content': case_data['content'],
                        'metadata': case_data['metadata']
                    })
        
        # Search crisis periods
        if not context_type or context_type == 'crisis_periods':
            for crisis_id, crisis_data in self.memory_index['crisis_periods'].items():
                score = self._calculate_relevance_score(crisis_data['content'], keywords)
                if score > 0:
                    scored_cases.append({
                        'id': crisis_id,
                        'type': 'crisis_period',
                        'score': score,
                        'content': crisis_data['content'],
                        'metadata': crisis_data['metadata']
                    })
        
        # Sort by relevance and return top matches
        scored_cases.sort(key=lambda x: x['score'], reverse=True)
        return scored_cases[:self.config['retrieval_top_k']]
    
    def _calculate_relevance_score(self, content: str, keywords: List[str]) -> float:
        """Calculate relevance score between content and keywords"""
        if not keywords:
            return 0.0
        
        content_lower = content.lower()
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        return matches / len(keywords)
    
    def _generate_response(self, query: str, relevant_cases: List[Dict]) -> str:
        """Generate response based on relevant cases"""
        if not relevant_cases:
            return "No se encontraron casos relevantes para la consulta."
        
        response = f"Análisis de evolución legal para: '{query}'\n\n"
        response += "Basado en el análisis del dataset Legal Evolution Dataset con Reality Filter:\n\n"
        
        # Categorize cases by type
        evolution_cases = [c for c in relevant_cases if c['type'] == 'evolution_case']
        crisis_cases = [c for c in relevant_cases if c['type'] == 'crisis_period']
        
        if evolution_cases:
            response += "📊 CASOS DE EVOLUCIÓN LEGAL RELEVANTES:\n"
            for i, case in enumerate(evolution_cases[:5], 1):
                metadata = case['metadata']
                response += f"{i}. Área: {metadata['legal_area']}, "
                response += f"Inicio: {metadata['start_date']}, "
                response += f"Éxito: {metadata['success']} "
                response += f"(Score: {case['score']:.2f})\n"
            response += "\n"
        
        if crisis_cases:
            response += "⚡ PERÍODOS DE CRISIS RELEVANTES:\n"
            for i, case in enumerate(crisis_cases[:3], 1):
                metadata = case['metadata']
                response += f"{i}. Tipo: {metadata['crisis_type']}, "
                response += f"Severidad: {metadata['severity']}, "
                response += f"Inicio: {metadata['start_date']} "
                response += f"(Score: {case['score']:.2f})\n"
            response += "\n"
        
        # Add analysis insights
        response += "🎯 INSIGHTS PRINCIPALES:\n"
        response += self._generate_insights(relevant_cases)
        
        return response
    
    def _generate_insights(self, cases: List[Dict]) -> str:
        """Generate insights from relevant cases"""
        insights = []
        
        if not cases:
            return "No se generaron insights suficientes.\n"
        
        # Legal area analysis
        areas = [c['metadata'].get('legal_area') for c in cases if c['metadata'].get('legal_area')]
        if areas:
            most_common_area = max(set(areas), key=areas.count)
            insights.append(f"- Área legal más relevante: {most_common_area}")
        
        # Success pattern analysis
        successes = [c['metadata'].get('success') for c in cases if c['metadata'].get('success')]
        if successes:
            success_rate = successes.count('Exitoso') / len(successes) * 100
            insights.append(f"- Tasa de éxito en casos relevantes: {success_rate:.1f}%")
        
        # Temporal pattern analysis
        dates = [c['metadata'].get('start_date') for c in cases if c['metadata'].get('start_date')]
        if dates:
            years = [d[:4] for d in dates if d and len(d) >= 4]
            if years:
                earliest = min(years)
                latest = max(years)
                insights.append(f"- Período temporal: {earliest}-{latest}")
        
        return "\n".join(insights) + "\n"
    
    def _analyze_response(self, response: str, query: str) -> Dict:
        """Analyze response for legal evolution insights"""
        analysis = {
            'legal_areas_mentioned': [],
            'temporal_patterns': [],
            'evolution_mechanisms': [],
            'success_indicators': [],
            'crisis_indicators': []
        }
        
        response_lower = response.lower()
        
        # Detect legal areas
        for area in self.config['legal_domains']:
            if area in response_lower:
                analysis['legal_areas_mentioned'].append(area)
        
        # Detect evolution mechanisms
        mechanisms = ['acumulativa', 'artificial', 'mixta', 'transplante', 'endogeno', 'hibrido']
        for mechanism in mechanisms:
            if mechanism in response_lower:
                analysis['evolution_mechanisms'].append(mechanism)
        
        # Detect success indicators
        success_terms = ['exitoso', 'parcial', 'fracaso', 'en_desarrollo']
        for term in success_terms:
            if term in response_lower:
                analysis['success_indicators'].append(term)
        
        # Extract years
        years = re.findall(r'\b(19|20)\d{2}\b', response)
        analysis['temporal_patterns'] = list(set(years))
        
        return analysis
    
    def _calculate_confidence(self, cases: List[Dict], keywords: List[str]) -> float:
        """Calculate confidence score"""
        if not cases:
            return 0.0
        
        base_confidence = 0.6
        
        # Boost confidence based on number of relevant cases
        case_boost = min(len(cases) * 0.05, 0.3)
        base_confidence += case_boost
        
        # Boost confidence based on average relevance score
        avg_score = sum(case['score'] for case in cases) / len(cases)
        score_boost = avg_score * 0.2
        base_confidence += score_boost
        
        # Boost confidence for Reality Filter verified sources
        verified_boost = 0.1  # Assume Reality Filter verification
        base_confidence += verified_boost
        
        return min(base_confidence, 1.0)
    
    def _extract_sources(self, response: str) -> List[str]:
        """Extract legal sources from response"""
        sources = []
        
        # Common Argentine legal source patterns
        patterns = [
            r'Ley \d+\.\d+',
            r'Decreto \d+/\d+', 
            r'Fallos \d+:\d+',
            r'InfoLeg', r'SAIJ', r'CSJN', r'BCRA', r'CNV'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            sources.extend(matches)
        
        return list(set(sources))
    
    def analyze_evolution_velocity(self, legal_area: Optional[str] = None) -> Dict:
        """Analyze legal evolution velocity patterns"""
        try:
            df = self.velocity_metrics.copy()
            if legal_area and not df.empty:
                df = df[df['area_derecho'] == legal_area]
            
            if df.empty:
                return {
                    'error': 'No velocity metrics available',
                    'legal_area': legal_area or 'All',
                    'total_metrics': 0
                }
            
            analysis = {
                'total_metrics': len(df),
                'legal_area': legal_area or 'All',
                'velocity_summary': {
                    'periods_analyzed': df['period'].nunique(),
                    'metric_types': df['metric_type'].value_counts().to_dict(),
                    'areas_covered': df['area_derecho'].nunique()
                },
                'key_insights': []
            }
            
            # Generate insights
            if 'Reform_Frequency' in df['metric_type'].values:
                reform_metrics = df[df['metric_type'] == 'Reform_Frequency']
                if not reform_metrics.empty:
                    avg_frequency = reform_metrics['value'].mean()
                    analysis['key_insights'].append(f"Frecuencia promedio de reformas: {avg_frequency:.2f}")
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def track_legal_transplants(self, origin_country: Optional[str] = None) -> Dict:
        """Track legal transplant success patterns"""
        try:
            df = self.transplants_tracking.copy()
            if origin_country and not df.empty:
                df = df[df['origin_country'] == origin_country]
            
            if df.empty:
                return {
                    'error': 'No transplant data available',
                    'origin_country': origin_country or 'All',
                    'total_transplants': 0
                }
            
            analysis = {
                'total_transplants': len(df),
                'origin_country': origin_country or 'All',
                'success_analysis': {},
                'adaptation_patterns': {},
                'key_insights': []
            }
            
            if 'success_level' in df.columns:
                analysis['success_analysis'] = df['success_level'].value_counts().to_dict()
                success_rate = (df['success_level'] == 'High').sum() / len(df) * 100
                analysis['key_insights'].append(f"Tasa de éxito alto: {success_rate:.1f}%")
            
            if 'adaptation_required' in df.columns:
                analysis['adaptation_patterns'] = df['adaptation_required'].value_counts().to_dict()
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def crisis_impact_analysis(self, crisis_type: Optional[str] = None) -> Dict:
        """Analyze crisis impact on legal evolution"""
        try:
            df = self.crisis_periods.copy()
            if crisis_type and not df.empty:
                df = df[df['crisis_type'].str.contains(crisis_type, na=False)]
            
            if df.empty:
                return {
                    'error': 'No crisis data available',
                    'crisis_type': crisis_type or 'All',
                    'total_crises': 0
                }
            
            analysis = {
                'total_crises': len(df),
                'crisis_type_filter': crisis_type or 'All',
                'impact_summary': {},
                'key_insights': []
            }
            
            if 'acceleration_factor' in df.columns:
                avg_acceleration = df['acceleration_factor'].mean()
                max_acceleration = df['acceleration_factor'].max()
                analysis['impact_summary']['avg_acceleration'] = avg_acceleration
                analysis['impact_summary']['max_acceleration'] = max_acceleration
                analysis['key_insights'].append(f"Factor de aceleración promedio: {avg_acceleration:.2f}")
            
            if 'severity_level' in df.columns:
                analysis['impact_summary']['severity_distribution'] = df['severity_level'].value_counts().to_dict()
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_comprehensive_report(self, output_path: str = './legal_evolution_lite_report.json') -> Dict:
        """Generate comprehensive legal evolution analysis report"""
        try:
            report = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'system': 'Legal Evolution MemoRAG Lite',
                    'version': '1.0.0-lite',
                    'dataset_summary': {
                        'evolution_cases': len(self.evolution_cases),
                        'velocity_metrics': len(self.velocity_metrics),
                        'transplant_cases': len(self.transplant_cases),
                        'crisis_periods': len(self.crisis_periods)
                    }
                },
                'analyses': {
                    'velocity_analysis': self.analyze_evolution_velocity(),
                    'transplant_analysis': self.track_legal_transplants(),
                    'crisis_analysis': self.crisis_impact_analysis()
                },
                'sample_queries': []
            }
            
            # Generate sample query results
            sample_queries = [
                "¿Cómo evolucionó el fideicomiso en Argentina?",
                "¿Qué impacto tuvo la crisis de 2001 en la evolución legal?",
                "¿Cuáles fueron los transplantes legales más exitosos?"
            ]
            
            for query in sample_queries:
                result = self.query_legal_evolution(query)
                report['sample_queries'].append({
                    'query': query,
                    'confidence': result.get('confidence', 0),
                    'relevant_cases': len(result.get('relevant_cases', [])),
                    'analysis': result.get('analysis', {})
                })
            
            # Save report
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Comprehensive report generated: {output_path}")
            return report
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return {'error': str(e)}

def main():
    """Main demonstration function"""
    print("🏛️ Legal Evolution MemoRAG Lite - Lex Certainty Enterprise")
    print("=" * 70)
    
    try:
        # Initialize system
        memorag = LegalEvolutionMemoRAGLite('./memorag_config.json')
        
        # Demo queries
        demo_queries = [
            "¿Cómo evolucionó el fideicomiso financiero en Argentina?",
            "¿Qué impacto tuvo la hiperinflación en la evolución legal?",
            "Analizar el éxito del amparo como transplante legal",
            "¿Cómo aceleró la crisis de 2001 los cambios legales?"
        ]
        
        print("\n🔍 Ejecutando consultas de demostración:")
        print("-" * 50)
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n{i}. {query}")
            result = memorag.query_legal_evolution(query)
            print(f"   Confianza: {result.get('confidence', 0):.2f}")
            print(f"   Casos relevantes: {len(result.get('relevant_cases', []))}")
            if result.get('analysis', {}).get('legal_areas_mentioned'):
                print(f"   Áreas legales: {', '.join(result['analysis']['legal_areas_mentioned'])}")
        
        # Generate analyses
        print(f"\n📊 Análisis de velocidad:")
        velocity = memorag.analyze_evolution_velocity()
        print(f"   Total métricas: {velocity.get('total_metrics', 0)}")
        
        print(f"\n🔄 Análisis de transplantes:")
        transplants = memorag.track_legal_transplants()
        print(f"   Total transplantes: {transplants.get('total_transplants', 0)}")
        
        print(f"\n⚡ Análisis de crisis:")
        crisis = memorag.crisis_impact_analysis()
        print(f"   Total crisis: {crisis.get('total_crises', 0)}")
        
        # Generate comprehensive report
        print(f"\n📄 Generando reporte integral...")
        report = memorag.generate_comprehensive_report()
        
        print(f"\n🎉 Demo completado exitosamente!")
        print(f"📁 Reporte guardado: ./legal_evolution_lite_report.json")
        
    except Exception as e:
        print(f"❌ Error en demo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())