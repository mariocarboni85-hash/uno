"""
Network and API Communication Tool
Handles HTTP requests, API interactions, webhooks
"""
import urllib.request
import urllib.parse
import urllib.error
import json
from typing import Dict, List, Optional, Any
import socket
import ssl
from datetime import datetime


class NetworkTool:
    """Advanced network and API operations."""
    
    def __init__(self):
        self.session_headers = {
            'User-Agent': 'Super-Agent/1.0'
        }
        self.request_history = []
    
    def http_request(self, url: str, method: str = 'GET',
                    headers: Optional[Dict] = None,
                    data: Optional[Dict] = None,
                    timeout: int = 30) -> Dict[str, Any]:
        """
        Make HTTP request.
        
        Args:
            url: Target URL
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: Custom headers
            data: Request data (for POST/PUT)
            timeout: Timeout in seconds
        """
        try:
            # Prepare headers
            req_headers = {**self.session_headers}
            if headers:
                req_headers.update(headers)
            
            # Prepare data
            req_data = None
            if data:
                if isinstance(data, dict):
                    req_data = json.dumps(data).encode('utf-8')
                    req_headers['Content-Type'] = 'application/json'
                elif isinstance(data, str):
                    req_data = data.encode('utf-8')
            
            # Create request
            request = urllib.request.Request(
                url,
                data=req_data,
                headers=req_headers,
                method=method
            )
            
            # Execute request
            start_time = datetime.now()
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = response.status
                response_headers = dict(response.headers)
                body = response.read().decode('utf-8')
                
                # Try to parse JSON
                try:
                    body_json = json.loads(body)
                except:
                    body_json = body
                
                duration = (datetime.now() - start_time).total_seconds()
                
                result = {
                    'success': True,
                    'status': status,
                    'headers': response_headers,
                    'body': body_json,
                    'duration': duration,
                    'url': url
                }
                
                # Record in history
                self.request_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'method': method,
                    'url': url,
                    'status': status,
                    'duration': duration
                })
                
                return result
        
        except urllib.error.HTTPError as e:
            return {
                'success': False,
                'error': f'HTTP {e.code}: {e.reason}',
                'status': e.code,
                'url': url
            }
        except urllib.error.URLError as e:
            return {
                'success': False,
                'error': f'URL Error: {e.reason}',
                'url': url
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'url': url
            }
    
    def get(self, url: str, headers: Optional[Dict] = None) -> Dict:
        """HTTP GET request."""
        return self.http_request(url, 'GET', headers=headers)
    
    def post(self, url: str, data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> Dict:
        """HTTP POST request."""
        return self.http_request(url, 'POST', headers=headers, data=data)
    
    def put(self, url: str, data: Optional[Dict] = None,
           headers: Optional[Dict] = None) -> Dict:
        """HTTP PUT request."""
        return self.http_request(url, 'PUT', headers=headers, data=data)
    
    def delete(self, url: str, headers: Optional[Dict] = None) -> Dict:
        """HTTP DELETE request."""
        return self.http_request(url, 'DELETE', headers=headers)
    
    def check_connection(self, host: str, port: int = 80, timeout: int = 5) -> Dict:
        """Check if host:port is reachable."""
        try:
            start_time = datetime.now()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                'reachable': result == 0,
                'host': host,
                'port': port,
                'duration': duration
            }
        except Exception as e:
            return {
                'reachable': False,
                'host': host,
                'port': port,
                'error': str(e)
            }
    
    def ping(self, host: str) -> Dict:
        """Ping host (check DNS and reachability)."""
        try:
            # DNS lookup
            start_time = datetime.now()
            ip_address = socket.gethostbyname(host)
            dns_time = (datetime.now() - start_time).total_seconds()
            
            # TCP connection test
            conn_result = self.check_connection(host, 80, timeout=3)
            
            return {
                'host': host,
                'ip': ip_address,
                'dns_resolved': True,
                'dns_time': dns_time,
                'reachable': conn_result['reachable'],
                'response_time': conn_result.get('duration', 0)
            }
        except socket.gaierror:
            return {
                'host': host,
                'dns_resolved': False,
                'error': 'DNS resolution failed'
            }
        except Exception as e:
            return {
                'host': host,
                'error': str(e)
            }
    
    def get_public_ip(self) -> Dict:
        """Get public IP address."""
        try:
            response = self.get('https://api.ipify.org?format=json')
            if response['success']:
                return {
                    'success': True,
                    'ip': response['body'].get('ip', 'unknown')
                }
            return response
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_ip_info(self, ip: Optional[str] = None) -> Dict:
        """Get information about IP address."""
        try:
            url = f'https://ipapi.co/{ip}/json/' if ip else 'https://ipapi.co/json/'
            response = self.get(url)
            
            if response['success']:
                return {
                    'success': True,
                    'info': response['body']
                }
            return response
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def download_data(self, url: str, save_path: Optional[str] = None) -> Dict:
        """Download data from URL."""
        try:
            response = self.http_request(url, 'GET')
            
            if response['success']:
                data = response['body']
                
                if save_path:
                    with open(save_path, 'w', encoding='utf-8') as f:
                        if isinstance(data, dict) or isinstance(data, list):
                            json.dump(data, f, indent=2)
                        else:
                            f.write(str(data))
                    
                    return {
                        'success': True,
                        'saved_to': save_path,
                        'size': len(str(data))
                    }
                
                return {
                    'success': True,
                    'data': data,
                    'size': len(str(data))
                }
            
            return response
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_ssl_certificate(self, host: str, port: int = 443) -> Dict:
        """Check SSL certificate details."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        # Parse certificate fields safely
                        subject_data = cert.get('subject', [])
                        issuer_data = cert.get('issuer', [])
                        
                        subject_dict = {}
                        if subject_data:
                            for item in subject_data:
                                if item and len(item) > 0:
                                    key_value = item[0]
                                    if isinstance(key_value, tuple) and len(key_value) == 2:
                                        subject_dict[key_value[0]] = key_value[1]
                        
                        issuer_dict = {}
                        if issuer_data:
                            for item in issuer_data:
                                if item and len(item) > 0:
                                    key_value = item[0]
                                    if isinstance(key_value, tuple) and len(key_value) == 2:
                                        issuer_dict[key_value[0]] = key_value[1]
                        
                        return {
                            'valid': True,
                            'subject': subject_dict,
                            'issuer': issuer_dict,
                            'version': cert.get('version'),
                            'serial_number': cert.get('serialNumber'),
                            'not_before': cert.get('notBefore'),
                            'not_after': cert.get('notAfter')
                        }
                    else:
                        return {
                            'valid': False,
                            'error': 'No certificate available'
                        }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def batch_request(self, urls: List[str], method: str = 'GET') -> List[Dict]:
        """Make multiple requests."""
        results = []
        
        for url in urls:
            result = self.http_request(url, method)
            results.append(result)
        
        return results
    
    def get_request_history(self, limit: int = 10) -> List[Dict]:
        """Get recent request history."""
        return self.request_history[-limit:]
    
    def clear_history(self):
        """Clear request history."""
        self.request_history = []


class APIClient:
    """Generic API client with authentication support."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None,
                 auth_header: str = 'Authorization'):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.auth_header = auth_header
        self.network = NetworkTool()
    
    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _get_headers(self, custom_headers: Optional[Dict] = None) -> Dict:
        """Build headers with authentication."""
        headers = {}
        
        if self.api_key:
            headers[self.auth_header] = f"Bearer {self.api_key}"
        
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def get(self, endpoint: str, params: Optional[Dict] = None,
           headers: Optional[Dict] = None) -> Dict:
        """GET request to API endpoint."""
        url = self._build_url(endpoint)
        
        if params:
            query_string = urllib.parse.urlencode(params)
            url = f"{url}?{query_string}"
        
        return self.network.get(url, headers=self._get_headers(headers))
    
    def post(self, endpoint: str, data: Optional[Dict] = None,
            headers: Optional[Dict] = None) -> Dict:
        """POST request to API endpoint."""
        url = self._build_url(endpoint)
        return self.network.post(url, data=data, headers=self._get_headers(headers))
    
    def put(self, endpoint: str, data: Optional[Dict] = None,
           headers: Optional[Dict] = None) -> Dict:
        """PUT request to API endpoint."""
        url = self._build_url(endpoint)
        return self.network.put(url, data=data, headers=self._get_headers(headers))
    
    def delete(self, endpoint: str, headers: Optional[Dict] = None) -> Dict:
        """DELETE request to API endpoint."""
        url = self._build_url(endpoint)
        return self.network.delete(url, headers=self._get_headers(headers))


# Global instances
_network = NetworkTool()

def http_get(url: str) -> Dict:
    """Simple HTTP GET."""
    return _network.get(url)

def http_post(url: str, data: Dict) -> Dict:
    """Simple HTTP POST."""
    return _network.post(url, data=data)

def ping(host: str) -> Dict:
    """Ping host."""
    return _network.ping(host)

def get_public_ip() -> Dict:
    """Get public IP."""
    return _network.get_public_ip()
